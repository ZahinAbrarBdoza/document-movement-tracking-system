from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/new/', views.document_create, name='document_create'),
    path('documents/export/', views.export_documents_excel, name='export_documents_excel'),
    path('documents/pending/', views.pending_documents, name='pending_documents'),
    path('documents/forwarded/', views.forwarded_documents, name='forwarded_documents'),
    path('documents/my-assigned/', views.my_assigned_documents, name='my_assigned_documents'),
    path('documents/bulk-forward/', views.bulk_forward_documents, name='bulk_forward_documents'),
    path('documents/bulk-close/', views.bulk_close_documents, name='bulk_close_documents'),
    path('documents/<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/<int:pk>/update/', views.document_update_movement, name='document_update_movement'),

    path('api/regions/', views.get_regions, name='get_regions'),
    path('api/areas/', views.get_areas, name='get_areas'),
    path('api/branches/', views.get_branches, name='get_branches'),
    path('api/courier-rate/', views.get_courier_rate, name='get_courier_rate'),

    path('reports/', views.reports_dashboard, name='reports_dashboard'),
]
