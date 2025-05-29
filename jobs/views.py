from django.shortcuts import render, redirect
# from django.core.mail import send_mail

# from django.contrib import messages


def jobs(request):
    context = {}
    return render(request, 'jobs/jobs.html', context)
