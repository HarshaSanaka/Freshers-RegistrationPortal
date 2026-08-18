from django.contrib import admin

from django.contrib import admin
from .models import StudentProfile, AcademicInformation

class AcademicInformationInline(admin.StackedInline):
    model = AcademicInformation
    can_delete = False
    verbose_name_plural = 'Academic Details'

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'user', 'gender', 'phone', 'status', 'created_at')
    list_filter = ('status', 'gender')
    search_fields = ('registration_number', 'user__first_name', 'user__last_name', 'user__email', 'phone')
    inlines = [AcademicInformationInline]