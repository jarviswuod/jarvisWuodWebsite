from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .forms import NewsletterForm
from .models import NewsletterSubscriber


def blogs(request):
    form = NewsletterForm()

    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            subscriber = form.save()
            send_newsletter_confirmation_email(
                request, subscriber.email_address)
            return redirect('newsletter_success')  # Redirect to success page
        else:
            messages.error(
                request, "You are already subscribed to our newsletter or invalid email.")

    context = {'form': form}
    return render(request, 'blogs/blogs.html', context)


def newsletter_subscription(request):
    """
    Dedicated newsletter subscription page
    """
    form = NewsletterForm()

    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            subscriber = form.save()
            send_newsletter_confirmation_email(
                request, subscriber.email_address)
            return redirect('newsletter_success')
        else:
            messages.error(
                request, "You are already subscribed to our newsletter or invalid email.")

    context = {'form': form}
    return render(request, 'blogs/newsletter_subscription.html', context)


def newsletter_success(request):
    """
    Success page for new newsletter subscribers
    """
    return render(request, 'blogs/newsletter_success.html')


# ////////////////////////////////////////////////////////////////////////////////////////////
# HELPER FUNCTIONS
# ////////////////////////////////////////////////////////////////////////////////////////////

def send_newsletter_confirmation_email(request, email_address):
    """
    Send newsletter confirmation email and handle success/error messaging
    """
    subject = "Welcome to Jarvis Wuod's Newsletter"
    message = f"""
    Hi there,

    Thank you for subscribing to my newsletter.

    You'll receive thoughtful content straight to your inbox every week.
    No spam, just valuable insights and updates on my latest blog posts.

    What to expect:
    - Weekly curated content
    - Exclusive insights and tips
    - Early access to new blog posts
    - Behind-the-scenes updates

    If you ever want to unsubscribe, simply click the unsubscribe link at the bottom of any newsletter email.

    Best regards,
    Jarvis Wuod
    """

    try:
        send_mail(subject, message, 'jarviswuod@gmail.com', [email_address])
        messages.success(
            request, "You have successfully subscribed to the weekly newsletter!")
    except Exception as e:
        messages.warning(
            request, "Subscription successful, but there was an issue sending the confirmation email.")
