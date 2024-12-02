from django.urls import path
from . import views

urlpatterns = [
    path('computers/list', views.ComputersListView.as_view(), name='computers_list'),
    path('computers/create', views.ComputersCreateView.as_view(), name='computers_create'),
    path('computers/<int:pk>/detail', views.ComputersDetailView.as_view(), name='computers_detail'),
    path('computers/<int:pk>/update', views.ComputersUpdateView.as_view(), name='computers_update'),
    path('computers/<int:pk>/delete', views.ComputersDeleteView.as_view(), name='computers_delete'),
    path('computers/export', views.export_data, name='computers_export'),
    path('computers/import', views.import_data, name='computers_import'),
    path('computers/<int:pk>/qr_code', views.qr_code_view, name='computers_qr_code'),
]    