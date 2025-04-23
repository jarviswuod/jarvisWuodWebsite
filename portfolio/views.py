
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from django.contrib import messages

from .models import MentorshipContact, ExpertiseContact, ResumeReviewContact
from .forms import MentorshipForm, ExpertiseForm, ResumeReviewForm


def home(request):
    context = {}
    return render(request, "home.html", context)


def about(request):
    context = {}
    return render(request, 'about.html', context)


def blogs(request):
    context = {}
    return render(request, 'blogs.html', context)


def services(request):
    context = {}
    return render(request, 'services.html', context)


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
    Your Team
    """
    send_mail(subject, message, 'your@email.com', [email])


def contact(request):
    mentorship_form = MentorshipForm()
    expertise_form = ExpertiseForm()
    resume_review_form = ResumeReviewForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'mentorship':
            print("Mentorship form submitted")
            print(request.POST)
            print(request.FILES)
            mentorship_form = MentorshipForm(request.POST)
            print(mentorship_form.data)
            if mentorship_form.is_valid():
                print("Mentorship form submitted")
                mentorship_contact = mentorship_form.save()
                send_confirmation_email(
                    name=mentorship_contact.full_name,
                    email=mentorship_contact.email_address,
                    service_type="Developer Mentorship Support Program"
                )
                messages.success(
                    request, "Thank you for your mentorship inquiry!")
                return redirect('contact')

        elif form_type == 'expertise':
            print("Expertise form submitted")
            print(request.POST)
            print(request.FILES)
            expertise_form = ExpertiseForm(request.POST)
            if expertise_form.is_valid():
                print("Expertise form submitted")

                expertise_contact = expertise_form.save()
                send_confirmation_email(
                    name=expertise_contact.full_name,
                    email=expertise_contact.email_address,
                    service_type="Hire an Expert"
                )
                messages.success(
                    request, "Thank you for your expertise inquiry!")
                return redirect('contact')

        elif form_type == 'resume_review':
            print("Resume Review form submitted")
            print(request.POST)
            print(request.FILES)
            resume_review_form = ResumeReviewForm(request.POST, request.FILES)
            print("Resume Review form submitted")

            if resume_review_form.is_valid():
                resume_review_contact = resume_review_form.save()
                send_confirmation_email(
                    name=resume_review_contact.full_name,
                    email=resume_review_contact.email_address,
                    service_type="Resume Review"
                )
                messages.success(
                    request, "Thank you for submitting your resume!")
                return redirect('contact')

    context = {
        'mentorship_form': mentorship_form,
        'expertise_form': expertise_form,
        'resume_review_form': resume_review_form,
    }

    return render(request, 'contact.html', context)
