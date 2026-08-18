from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.verification_dashboard, name='verification_dashboard'),
    path('review/<int:pk>/', views.student_verification_detail, name='student_verification_detail'),
    path('admission-slip/<int:pk>/', views.admission_slip, name='admission_slip'),
]