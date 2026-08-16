from django.urls import path
from . import views

urlpatterns = [
    path('my-documents/', views.document_list_view, name='document_list'),
    path('verify/<int:pk>/<str:status>/', views.admin_verify_document, name='verify_document'),
]