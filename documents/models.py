import os
import subprocess

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from core.models import Department
from django.db import models


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

    def is_convertible(self):
        return self.extension in ['docx', 'xlsx', 'pptx', 'xls', 'csv']

    def get_conversion_paths(self):
        input_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
        output_dir = os.path.join(settings.MEDIA_ROOT, 'documents/pdf/')
        os.makedirs(output_dir, exist_ok=True)
        original_name = os.path.splitext(os.path.basename(self.file.name))[0]
        output_path = os.path.join(output_dir, f"{original_name}.pdf")
        return input_path, output_path

    def convert_to_pdf(self, input_path, output_dir):
        try:
            subprocess.run([
                'soffice',
                '--headless',
                '--convert-to', 'pdf',
                input_path,
                '--outdir', output_dir
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"PDF conversion failed: {e}")

    def attach_pdf_file(self, output_path, filename):
        if os.path.exists(output_path):
            with open(output_path, 'rb') as f:
                self.pdf_file.save(filename, File(f), save=False)
            super().save(update_fields=['pdf_file'])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        input_path, output_path = self.get_conversion_paths()
        filename = os.path.basename(output_path)

        if self.extension == 'pdf':
            if os.path.exists(input_path):
                os.rename(input_path, output_path)
                with open(output_path, 'rb') as f:
                    self.pdf_file.save(filename, File(f), save=False)
                self.save(update_fields=['pdf_file'])

        elif self.is_convertible():
            self.convert_to_pdf(input_path, os.path.dirname(output_path))
            self.attach_pdf_file(output_path, filename)

    def __str__(self):
        return self.title
