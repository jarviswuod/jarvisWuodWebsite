from django.shortcuts import render, redirect, reverse
from .forms import BookCallForm, MentorshipForm, ExpertiseForm, ResumeReviewForm

from django.contrib import messages
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, Http404

from blogs.models import Blog

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import logging
logger = logging.getLogger(__name__)


def about(request):
    context = {}

    return render(request, 'main/about.html', context)


def pricing(request):
    context = {}

    return render(request, 'main/pricing.html', context)


def home(request):
    book_call_form = BookCallForm()
    blogs = Blog.objects.filter(is_published=True)[:3]

    if request.method == 'POST':
        book_call_form = BookCallForm(request.POST)
        if book_call_form.is_valid():
            book_call_contact = book_call_form.save()
            full_name = book_call_contact.full_name
            email = book_call_contact.email_address

            first_free_call_email_confirmation(
                request=request, full_name=full_name, email=email)

            return redirect('home')

    context = {'book_call_form': book_call_form, "blogs": blogs}
    return render(request, "main/home.html", context)


def contact(request):
    mentorship_form = MentorshipForm()
    expertise_form = ExpertiseForm()
    resume_review_form = ResumeReviewForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'mentorship':
            mentorship_form = MentorshipForm(request.POST)

            if mentorship_form.is_valid():
                mentorship_contact = mentorship_form.save()
                subject = 'Your Call Booking Confirmation Developer Mentorship Support Program'
                message = 'Thank you for booking a call...'
                email = mentorship_contact.email_address

                contact_page_boooking_email_confirmation(
                    request=request, subject=subject, message=message, email=email)

        elif form_type == 'expertise':
            expertise_form = ExpertiseForm(request.POST)

            if expertise_form.is_valid():
                expertise_contact = expertise_form.save()
                subject = 'Your Call Booking Confirmation Hire an Expert'
                message = 'Thank you for booking a call...'
                email = expertise_contact.email_address

                contact_page_boooking_email_confirmation(
                    request=request, subject=subject, message=message, email=email)

        elif form_type == 'resume_review':
            resume_review_form = ResumeReviewForm(request.POST, request.FILES)

            if resume_review_form.is_valid():
                resume_review_contact = resume_review_form.save()
                subject = 'Your Call Booking Confirmation Resume Review Service'
                message = 'Thank you for booking a call...'
                email = resume_review_contact.email_address

                contact_page_boooking_email_confirmation(
                    request=request, subject=subject, message=message, email=email)

        return redirect(f"{reverse('contact')}#contact-selection")

    context = {
        'mentorship_form': mentorship_form,
        'expertise_form': expertise_form,
        'resume_review_form': resume_review_form,
    }

    return render(request, 'main/contact.html', context)


@staff_member_required
def view_log_file(request, filename):
    file_path = settings.BASE_DIR / 'logs' / filename

    if not file_path.exists():
        raise Http404("Log file not found.")

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit
    if file_path.stat().st_size > MAX_FILE_SIZE:
        return HttpResponse("File too large to display.", status=413)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            content = file.read()
            return HttpResponse(content, content_type='text/plain; charset=utf-8')
    except (IOError, OSError):
        raise Http404("Could not read log file.")


# ////////////////////////////////////////////////////////////////////////////////////////////
# HELPER FUCNTIONS
# ////////////////////////////////////////////////////////////////////////////////////////////


def first_free_call_email_confirmation(request, full_name, email):
    subject = "Web Development Mentorship Free Call Booking"
    message = f"""
    Hi {full_name},

    Your application for web development mentorship program has been successfuly received.

    Details:
        Name: {full_name}
        Email: {email}
        Interest: Web development Mentorship Program

    I will get back to you shortly.

    Regards,
    Jarvis
    """

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject=subject,
        plain_text_content=message
    )

    try:
        sg = SendGridAPIClient(
            api_key=settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent successfully: {response.status_code}")
        messages.success(
            request, "Thank you for booking a call! Kindly check your inbox or spam folder for confirmation email.")
    except Exception as sendgrid_error:
        logger.error(f"SendGrid error: {sendgrid_error}")
        messages.error(
            request, "There was an error with your submission. Please check the form and try again.")


def contact_page_boooking_email_confirmation(request, subject, message, email):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject=subject,
        plain_text_content=message
    )

    try:
        sg = SendGridAPIClient(
            api_key=settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Email sent successfully: {response.status_code}")
        messages.success(
            request, "Successfully submited Your request. Kindly check your inbox or spam folder for confirmation email.")
    except Exception as sendgrid_error:
        logger.error(f"SendGrid error: {sendgrid_error}")
        messages.error(
            request, "There was an error with your submission. Please check the form and try again.")
