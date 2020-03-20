from django.conf import settings


def site(request):
    return {
        'DEBUG': settings.DEBUG,
        'GOOGLE_ANALYTICS_TRACKING_ID': settings.GOOGLE_ANALYTICS_TRACKING_ID
    }
