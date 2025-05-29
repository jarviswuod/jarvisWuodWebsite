
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import BookCallForm

from django.contrib import messages


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


def about(request):
    context = {}

    return render(request, 'main/about.html', context)


def pricing(request):
    context = {}

    return render(request, 'main/pricing.html', context)


def contact(request):
    context = {}

    return render(request, 'main/contact.html', context)


# ////////////////////////////////////////////////////////////////////////////////////////////
# HELPER FUCNTIONS
# ////////////////////////////////////////////////////////////////////////////////////////////


def send_confirmation_email(name, email):
    subject = "Application Received"
    message = f"""
    Hi {name},

    Your application for web development mentorhip program has been successfuly received.

    Details:
        Name: {name}
        Email: {email}
        Interest: Web development Mentorship Program

    I will get back to you shortly.

    Regards,
    Jarvis
    """
    send_mail(subject, message, 'jarviswuod@gmail.com', [email])
