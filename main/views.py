
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from django.contrib import messages


def home(request):
    context = {}

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
