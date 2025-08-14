from django.shortcuts import redirect
from .utils import is_employee

class HelpdeskAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/helpdesk/') and not path.startswith('/helpdesk/no-access/') and not is_employee(request.user):
            return redirect('no_access')

        return self.get_response(request)
