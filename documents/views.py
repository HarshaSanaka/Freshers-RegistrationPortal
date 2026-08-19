from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .models import StudentDocument
from .forms import DocumentUploadForm

@login_required
@never_cache
def document_list_view(request):
    """Student portal for managing their document uploads."""
    documents = StudentDocument.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc_type = form.cleaned_data['document_type']
            uploaded_file = form.cleaned_data['file']

            # Update if already exists, or create a new entry
            doc, created = StudentDocument.objects.update_or_create(
                user=request.user,
                document_type=doc_type,
                defaults={'file': uploaded_file, 'status': 'PENDING', 'rejection_reason': ''}
            )
            messages.success(request, f"{doc.get_document_type_display()} uploaded successfully!")
            return redirect('document_list')
    else:
        form = DocumentUploadForm()

    return render(request, 'documents/document_list.html', {
        'documents': documents,
        'form': form,
    })

@user_passes_test(lambda u: u.is_staff)
def admin_verify_document(request, pk, status):
    """Admin action to approve or reject an individual document."""
    doc = get_object_or_404(StudentDocument, pk=pk)
    if status in ['APPROVED', 'REJECTED', 'PENDING']:
        doc.status = status
        if status == 'REJECTED':
            doc.rejection_reason = request.POST.get('reason', 'Document illegible or incorrect.')
        else:
            doc.rejection_reason = ''
        doc.save()
    return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))