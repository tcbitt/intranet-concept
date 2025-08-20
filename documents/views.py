from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

from .forms import DocumentUploadForm
from .models import Document, Department, Folder


def department_overview(request):
    departments = Department.objects.all()
    return render(request, 'documents/department_overview.html', {'departments': departments})


def department_documents(request, department_slug):
    department = get_object_or_404(Department, slug=department_slug)
    folders = Folder.objects.filter(department=department, parent__isnull=True)
    documents = Document.objects.filter(department=department, folder__isnull=True)

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.department = department
            document.save()
    else:
        form = DocumentUploadForm()

    return render(request, 'documents/department_overview.html', {
        'department': department,
        'folders': folders,
        'documents': documents,
        'form': form,
    })


def folder_view(request, department_slug, folder_id):
    department = get_object_or_404(Department, slug=department_slug)
    current_folder = get_object_or_404(Folder, id=folder_id, department=department)
    subfolders = current_folder.subfolders.all()
    documents = current_folder.documents.all()

    context = {
        'department': department,
        'current_folder': current_folder,
        'subfolders': subfolders,
        'documents': documents,
    }
    return render(request, 'documents/folder_view.html', context)


def documents_widget(request):
    folders = Folder.objects.select_related('department').all().order_by('name')
    return render(request, 'documents/widget.html', {'folders': folders})


def document_detail(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/detail_widget.html', {'document': doc})
