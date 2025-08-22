from django.conf import settings

def settings_context(request):
    return {
        'SHOW_ENV_BANNER': getattr(settings, 'SHOW_ENV_BANNER', False),
    }
