from django.contrib import admin
from .models import Document, Folder

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'department', 'folder')
    list_filter = ('department', 'folder')
    search_fields = ('title', 'description')

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'parent')
    list_filter = ('department',)
    search_fields = ('name',)


