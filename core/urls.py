from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from core.forms import StyledLoginForm

urlpatterns = [
    path('', views.home, name='home'),
    path('tool-truck-calendar/', views.tool_truck_calendar, name='tool-truck-calendar'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=StyledLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
