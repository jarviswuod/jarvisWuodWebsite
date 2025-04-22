
from django.shortcuts import render, redirect
from django.core.mail import send_mail

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


def save_form_data(mentorship_form, expertise_form, resumeReview_form):
    if mentorship_form.is_valid():
        mentorship_form.save()
    if expertise_form.is_valid():
        expertise_form.save()
    if resumeReview_form.is_valid():
        resumeReview_form.save()


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


# def contact(request):
#     if request.method == 'POST':
#         mentorship_form = MentorshipForm(request.POST)
#         expertise_form = ExpertiseForm(request.POST)
#         resumeReview_form = ResumeReviewForm(request.POST, request.FILES)

#         if all([
#             mentorship_form.is_valid(),
#             expertise_form.is_valid(),
#             resumeReview_form.is_valid()
#         ]):
#             save_form_data(mentorship_form, expertise_form, resumeReview_form)

#             # Use one of the valid forms to extract email details (example: mentorship)
#             contact_data = mentorship_form.cleaned_data
#             send_confirmation_email(
#                 name=contact_data['full_name'],
#                 email=contact_data['email_address'],
#                 service_type="Mentorship/Expertise/Resume Review"
#             )
#             return redirect('success')
#     else:
#         mentorship_form = MentorshipForm()
#         expertise_form = ExpertiseForm()
#         resumeReview_form = ResumeReviewForm()

#     context = {
#         'mentorship_form': mentorship_form,
#         'expertise_form': expertise_form,
#         'resumeReview_form': resumeReview_form,
#     }
#     return render(request, 'contact.html', context)

def contact(request):
    if request.method == 'POST':
        fullName = request.POST.get('fullName')
        emailAddress = request.POST.get('emailAddress')
        phoneNumber = request.POST.get('phoneNumber')
        startCoding = request.POST.get('startCoding')
        goal = request.POST.get('goal')
        obstacle = request.POST.get('obstacle')
        progressDetails = request.POST.get('progressDetails')

        mentorship_form = MentorshipContact(
            full_name=fullName,
            email_address=emailAddress,
            phone_number=phoneNumber,
            start_coding=startCoding,
            goal=goal,
            obstacle=obstacle,
            progress_details=progressDetails
        )
        mentorship_form.save()
        send_confirmation_email(
            name=fullName,
            email=emailAddress,
            service_type="Mentorship"
        )

        fullName = request.POST.get('fullName')
        emailAddress = request.POST.get('emailAddress')
        phoneNumber = request.POST.get('phoneNumber')
        serviceType = request.POST.get('serviceType')
        projectLink = request.POST.get('projectLink')
        projectDetails = request.POST.get('projectDetails')
        expertise_form = ExpertiseContact(
            full_name=fullName,
            email_address=emailAddress,
            phone_number=phoneNumber,
            service_type=serviceType,
            project_link=projectLink,
            project_details=projectDetails
        )
        expertise_form.save()
        send_confirmation_email(
            name=fullName,
            email=emailAddress,
            service_type="Expertise"
        )
        fullName = request.POST.get('fullName')
        emailAddress = request.POST.get('emailAddress')
        phoneNumber = request.POST.get('phoneNumber')
        resumeFrequency = request.POST.get('resumeFrequency')
        resumeReviewedBefore = request.POST.get('resumeReviewedBefore')
        uploadedResume = request.FILES.get('uploadedResume')
        linkedinProfile = request.POST.get('linkedinProfile')
        portfolioLinks = request.POST.get('portfolioLinks')
        jobHuntingExperience = request.POST.get('jobHuntingExperience')

        resumeReview_form = ResumeReviewContact(
            full_name=fullName,
            email_address=emailAddress,
            phone_number=phoneNumber,
            resume_frequency=resumeFrequency,
            resume_reviewed_before=resumeReviewedBefore,
            uploaded_resume=uploadedResume,
            linkedin_profile=linkedinProfile,
            portfolio_links=portfolioLinks
        )
        resumeReview_form.save()
        send_confirmation_email(
            name=fullName,
            email=emailAddress,
            service_type="Resume Review"
        )

    context = {}
    return render(request, 'contact.html', context)
