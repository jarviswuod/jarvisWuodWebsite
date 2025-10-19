from django.conf import settings


def global_debug(request):
    return {'debug': settings.DEBUG}


def google_analytics(request):
    return {"GA_ID": settings.GA_ID}
