from .utils import user_has_role

def support_role(request):
    return {
        'is_support': user_has_role(request.user, 'Support') if request.user.is_authenticated else False
    }