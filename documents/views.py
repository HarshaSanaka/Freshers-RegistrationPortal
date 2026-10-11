from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import StudentDocument


@login_required
def document_list_view(request):
	documents = StudentDocument.objects.filter(user=request.user).order_by('-uploaded_at')
	return render(request, 'documents/document_list.html', {'documents': documents})


@user_passes_test(lambda user: user.is_staff)
@require_POST
def admin_verify_document(request, pk, status):
	document = get_object_or_404(StudentDocument, pk=pk)
	allowed_statuses = {value for value, _label in StudentDocument.STATUS_CHOICES}

	if status in allowed_statuses:
		document.status = status
		document.rejection_reason = (
			request.POST.get('rejection_reason', '').strip()
			if status == 'REJECTED'
			else ''
		)
		document.save(update_fields=['status', 'rejection_reason', 'updated_at'])

	return redirect('admin_dashboard')
