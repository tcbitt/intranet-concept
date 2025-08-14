from django.urls import path
from . import views

urlpatterns = [
    path('', views.documents_widget, name='document-list'),
    path('<int:pk>/', views.document_detail, name='document-detail'),
    path('departments/', views.department_overview, name='department-overview'),
    path('departments/<slug:department_slug>/documents/', views.department_documents, name='department-documents'),
    path('departments/<slug:department_slug>/', views.folder_view, name='folder-view'),
    path('departments/<slug:department_slug>/folder/<int:folder_id>/', views.folder_view, name='folder-view'),
]
