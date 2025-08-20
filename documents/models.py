import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from docx2pdf import convert


class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Folder(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='folders')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')

    def get_ancestors(self):
        ancestors = []
        folder = self.parent
        while folder:
            ancestors.insert(0, folder)
            folder = folder.parent
        return ancestors

    def __str__(self):
        return f"{self.department.name} / {self.name}"

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='documents', null=True,
                                   blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')

    pdf_file = models.FileField(upload_to='documents/pdf/', blank=True, null=True)

    @property
    def extension(self):
        return self.file.name.split('.')[-1].lower()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        supported = ['docx', 'xlsx', 'pptx', 'xls']
        ext = self.extension

        if ext in supported:
            input_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
            output_dir = os.path.join(settings.MEDIA_ROOT, 'documents/pdf/')
            os.makedirs(output_dir, exist_ok=True)

            # Use LibreOffice for conversion
            output_path = os.path.join(output_dir, f"{self.pk}.pdf")
            os.system(f'soffice --headless --convert-to pdf "{input_path}" --outdir "{output_dir}"')

            self.pdf_file.name = os.path.relpath(output_path, settings.MEDIA_ROOT)
            super().save(update_fields=['pdf_file'])

    def __str__(self):
        return self.title




