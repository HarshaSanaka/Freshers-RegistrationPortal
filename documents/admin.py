from django.contrib import admin
from .models import StudentDocument

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'status', 'file')
    list_filter = ('status', 'document_type')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')