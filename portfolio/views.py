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


def contact(request):
    context = {}
    return render(request, 'contact.html', context)


def jobs(request):
    context = {}
    return render(request, 'jobs.html', context)
