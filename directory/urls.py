from django.urls import path
from .views import widget_view

urlpatterns = [
    path('', widget_view, name='directory-widget'),
]