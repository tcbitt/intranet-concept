from django.urls import path
from .views import view_document

app_name = 'fileviewer'

urlpatterns = [
    path('<int:pk>/', view_document, name='view-document'),
]
