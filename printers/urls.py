from django.urls import path
from . import views

urlpatterns = [
    path('printers/list', views.PrintersListView.as_view(), name='printers_list'),
    path('printers/create', views.PrintersCreateView.as_view(), name='printers_create'),
    path('printers/<int:pk>/detail', views.PrintersDetailView.as_view(), name='printers_detail'),
    path('printers/<int:pk>/update', views.PrintersUpdateView.as_view(), name='printers_update'),
    path('printers/<int:pk>/delete', views.PrintersDeleteView.as_view(), name='printers_delete'),
    path('printers/export', views.export_data, name='printers_export'),
    path('printers/import', views.import_data, name='printers_import'),
    path('printers/<int:pk>/qr_code', views.qr_code_view, name='printers_qr_code'),
]    