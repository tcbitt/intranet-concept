from django.shortcuts import render, get_object_or_404
from documents.models import Document

from django.shortcuts import render, get_object_or_404
from documents.models import Document

def view_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    office_extensions = ['docx', 'xlsx', 'pptx']

    # Build the full URL to the file
    absolute_file_url = request.build_absolute_uri(document.file.url)

    return render(request, 'fileviewer/viewer.html', {
        'document': document,
        'office_extensions': office_extensions,
        'absolute_file_url': absolute_file_url,
    })
