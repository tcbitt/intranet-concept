from django.contrib.auth.views import LoginView
from django.shortcuts import render
from core.forms import StyledLoginForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = StyledLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        return context

def home(request):
    return render(request, 'core/home.html')

def tool_truck_calendar(request):
    return render(request, 'core/tool_truck_calendar.html')