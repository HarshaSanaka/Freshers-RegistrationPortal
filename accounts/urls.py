from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('complete-profile/', views.complete_profile_view, name='complete_profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('status/<int:pk>/<str:status>/', views.update_status, name='update_status'),
    path('logout/', views.logout_view, name='logout'),
]