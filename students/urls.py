from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('academics/', views.view_academics, name='view_academics'),
    path('academics/edit/', views.edit_academics, name='edit_academics'),
]