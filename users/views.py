from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.template.loader import render_to_string
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.utils.http import url_has_allowed_host_and_scheme

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(
            self.request, f'Account created for {username}! You can now log in.')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('main:home')
    http_method_names = ['get', 'post']


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Override the default send_mail method to use SendGrid
        """
        # Render the subject
        subject = render_to_string(subject_template_name, context).strip()

        # Render the email content
        html_content = render_to_string(
            html_email_template_name or email_template_name, context)
        text_content = render_to_string(
            email_template_name, context) if html_email_template_name else html_content

        message = Mail(
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
            plain_text_content=text_content
        )

        try:
            sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            response = sg.send(message)
            logger.info(
                f"Password reset email sent! Status code: {response.status_code}")
        except Exception as sendgrid_error:
            logger.error(f"SendGrid error: {sendgrid_error}")
            raise

    def form_valid(self, form):
        messages.success(self.request, 'Password reset email has been sent!')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        messages.success(
            self.request, 'Your password has been reset successfully!')
        return super().form_valid(form)


def dashboard(request):
    return render(request, 'users/dashboard.html')


def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')


def password_reset_complete(request):
    return render(request, 'users/password_reset_complete.html')
