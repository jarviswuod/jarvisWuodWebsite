from django.shortcuts import render

# Create your views here.


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


def resume_review(request):
    context = {}
    return render(request, 'resume_review.html', context)


def web_dev(request):
    context = {}
    return render(request, 'web_dev.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)


def jobs(request):
    context = {}
    return render(request, 'jobs.html', context)
