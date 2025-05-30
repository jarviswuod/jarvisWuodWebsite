
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import BookCallForm, MentorshipForm, ExpertiseForm, ResumeReviewForm

from django.contrib import messages


def about(request):
    context = {}

    return render(request, 'main/about.html', context)


def pricing(request):
    context = {}

    return render(request, 'main/pricing.html', context)


def home(request):
    book_call_form = BookCallForm()

    if request.method == 'POST':
        book_call_form = BookCallForm(request.POST)
        if book_call_form.is_valid():
            book_call_contact = book_call_form.save()

            try:
                send_confirmation_email(
                    name=book_call_contact.full_name,
                    email=book_call_contact.email_address,
                )
                messages.success(
                    request, "Thank you for booking a call!")

            except Exception as e:
                print(f"Email error: {e}")
                messages.error(
                    request, "There was an error with your submission. Please check the form and try again.")

            return redirect('home')

    context = {'book_call_form': book_call_form}
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

                send_mail(
                    'Your Call Booking Confirmation Developer Mentorship Support Program',
                    'Thank you for booking a call...',
                    'jarviswuod@gmail.com',
                    [mentorship_contact.email_address],
                    fail_silently=False,
                )
                messages.success(
                    request, "Thank you for your mentorship inquiry!")
                return redirect('contact')

        elif form_type == 'expertise':
            expertise_form = ExpertiseForm(request.POST)

            if expertise_form.is_valid():
                expertise_contact = expertise_form.save()

                send_mail(
                    'Your Call Booking Confirmation Hire an Expert',
                    'Thank you for booking a call...',
                    'jarviswuod@gmail.com',
                    [expertise_contact.email_address],
                    fail_silently=False,
                )
                messages.success(
                    request, "Thank you for your expertise inquiry!")
                return redirect('contact')

        elif form_type == 'resume_review':
            resume_review_form = ResumeReviewForm(request.POST, request.FILES)

            if resume_review_form.is_valid():
                resume_review_contact = resume_review_form.save()

                send_mail(
                    'Your Call Booking Confirmation Resume Review Service',
                    'Thank you for booking a call...',
                    'jarviswuod@gmail.com',
                    [resume_review_contact.email_address],
                    fail_silently=False,
                )
                messages.success(
                    request, "Thank you for submitting your resume!")
                return redirect('contact')

    context = {
        'mentorship_form': mentorship_form,
        'expertise_form': expertise_form,
        'resume_review_form': resume_review_form,
    }

    return render(request, 'main/contact.html', context)


# ////////////////////////////////////////////////////////////////////////////////////////////
# HELPER FUCNTIONS
# ////////////////////////////////////////////////////////////////////////////////////////////


def send_confirmation_email(name, email):
    subject = "Application Received"
    message = f"""
    Hi {name},

    Your application for web development mentorship program has been successfuly received.

    Details:
        Name: {name}
        Email: {email}
        Interest: Web development Mentorship Program

    I will get back to you shortly.

    Regards,
    Jarvis
    """
    send_mail(subject, message, 'jarviswuod@gmail.com', [email])
