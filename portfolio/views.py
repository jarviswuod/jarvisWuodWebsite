
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from django.contrib import messages

from .forms import BookCallForm, MentorshipForm, ExpertiseForm, ResumeReviewForm, NewsletterForm
from .tasks import send_confirmation_email_celery


def home(request):
    book_call_form = BookCallForm()

    if request.method == 'POST':
        book_call_form = BookCallForm(request.POST)
        if book_call_form.is_valid():
            book_call_contact = book_call_form.save()
            try:

                send_confirmation_email_celery.delay(
                    subject='Your Call Booking Confirmation',
                    message='Thank you for booking a call...',
                    from_email='jarviswuod@gmail.com',
                    recipient_list=[
                        book_call_form.cleaned_data['email_address']]
                )
                # send_confirmation_email(
                #     name=book_call_contact.full_name,
                #     email=book_call_contact.email_address,
                #     service_type="Booked a Call"
                # )
            except Exception as e:
                print(f"Email error: {e}")

            messages.success(
                request, "Thank you for booking a call!")
            return redirect('home')

    context = {'book_call_form': book_call_form}
    return render(request, "home.html", context)


def about(request):
    context = {}
    return render(request, 'about.html', context)


def pricing(request):
    context = {}
    return render(request, 'pricing.html', context)


def mentorship(request):
    context = {}
    return render(request, 'mentorship.html', context)


def resume(request):
    context = {}
    return render(request, 'resume.html', context)


def software(request):
    context = {}
    return render(request, 'software.html', context)


def jobs(request):
    context = {}
    return render(request, 'jobs.html', context)


def send_confirmation_email(name, email, service_type):
    subject = "Application Received"
    message = f"""
    Hi {name},

    We’ve received your application for "{service_type}" and are reviewing it.

    Details:
        Name: {name}
        Email: {email}
        Type: {service_type}

    We'll contact you soon.

    Regards,
    Jarvis
    """
    send_mail(subject, message, 'your@email.com', [email])


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
                send_confirmation_email_celery.delay(
                    subject='Your Call Booking Confirmation',
                    message='Thank you for booking a call...',
                    from_email='jarviswuod@gmail.com',
                    recipient_list=[
                        mentorship_contact.cleaned_data['email_address']]
                )
                # send_confirmation_email(
                #     name=mentorship_contact.full_name,
                #     email=mentorship_contact.email_address,
                #     service_type="Developer Mentorship Support Program"
                # )
                messages.success(
                    request, "Thank you for your mentorship inquiry!")
                return redirect('contact')

        elif form_type == 'expertise':
            expertise_form = ExpertiseForm(request.POST)
            if expertise_form.is_valid():
                expertise_contact = expertise_form.save()
                send_confirmation_email_celery.delay(
                    subject='Your Call Booking Confirmation',
                    message='Thank you for booking a call...',
                    from_email='jarviswuod@gmail.com',
                    recipient_list=[
                        expertise_contact.cleaned_data['email_address']]
                )
                # send_confirmation_email(
                #     name=expertise_contact.full_name,
                #     email=expertise_contact.email_address,
                #     service_type="Hire an Expert"
                # )
                messages.success(
                    request, "Thank you for your expertise inquiry!")
                return redirect('contact')

        elif form_type == 'resume_review':
            resume_review_form = ResumeReviewForm(request.POST, request.FILES)
            if resume_review_form.is_valid():
                resume_review_contact = resume_review_form.save()
                send_confirmation_email_celery.delay(
                    subject='Your Call Booking Confirmation',
                    message='Thank you for booking a call...',
                    from_email='jarviswuod@gmail.com',
                    recipient_list=[
                        resume_review_contact.cleaned_data['email_address']]
                )
                # send_confirmation_email(
                #     name=resume_review_contact.full_name,
                #     email=resume_review_contact.email_address,
                #     service_type="Resume Review"
                # )
                messages.success(
                    request, "Thank you for submitting your resume!")
                return redirect('contact')

    context = {
        'mentorship_form': mentorship_form,
        'expertise_form': expertise_form,
        'resume_review_form': resume_review_form,
    }

    return render(request, 'contact.html', context)


def blogs(request):

    form = NewsletterForm()
    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']

            # Save subscriber to database
            subscriber = form.save()

            # Send confirmation email
            subject = "Welcome to Jarvis Wuod's Newsletter"
            message = f"""
            Hi there,
            
            Thank you for subscribing to my newsletter. 
            
            You'll receive thoughtful content straight to your inbox. 
            No spam, just valuable insights.
            
            If you ever want to unsubscribe, simply click the unsubscribe link at the bottom of any newsletter email.
            
            Best regards,
            Jarvis Wuod
            """
            # from_email = settings.DEFAULT_FROM_EMAIL
            # recipient_list = [email_address]

            try:
                # send_mail(subject, message, 'your@email.com',
                #           [email_address], fail_silently=False)
                send_confirmation_email_celery.delay(
                    subject='Your Call Booking Confirmation',
                    message='Thank you for booking a call...',
                    from_email='jarviswuod@gmail.com',
                    recipient_list=[email_address]
                )
                messages.success(request, "You have successfully subscribed!")
            except Exception as e:

                messages.warning(
                    request, "Subscription successful, but there was an issue sending the confirmation email.")

            return redirect('blogs')
        else:
            messages.error(
                request, "There was an error with your submission. Please check the form and try again.")

    context = {'form': form}

    return render(request, 'blogs.html', context)
