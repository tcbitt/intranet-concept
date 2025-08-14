from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_tickets, name='my_tickets'),
    path('all/', views.ticket_list, name='ticket_list'),
    path('new/', views.ticket_create, name='ticket_create'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('no-access/', views.no_access, name='no_access'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
]
