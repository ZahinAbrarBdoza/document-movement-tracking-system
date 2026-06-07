from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/new/', views.document_create, name='document_create'),
    path('documents/export/', views.export_documents_excel, name='export_documents_excel'),
    path('documents/pending/', views.pending_documents, name='pending_documents'),
    path('documents/<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/<int:pk>/update/', views.document_update_movement, name='document_update_movement'),

    path('reports/', views.reports_dashboard, name='reports_dashboard'),
]