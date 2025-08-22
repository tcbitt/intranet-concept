import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from documents.models import Document

@receiver(post_delete, sender=Document)
def delete_document_files(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)

    if instance.pdf_file and os.path.isfile(instance.pdf_file.path):
        os.remove(instance.pdf_file.path)

    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)
