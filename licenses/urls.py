from django.urls import path
from . import views

urlpatterns = [
    path('licenses/list', views.LicenseListView.as_view(), name='licenses_list'),
    path('licenses/create', views.LicenseCreateView.as_view(), name='licenses_create'),
    path('licenses/<int:pk>/detail', views.LicenseDetailView.as_view(), name='licenses_detail'),
    path('licenses/<int:pk>/update', views.LicenseUpdateView.as_view(), name='licenses_update'),
    path('licenses/<int:pk>/delete', views.LicenseDeleteView.as_view(), name='licenses_delete'),
    path('licenses/export', views.export_data, name='licenses_export'),
    path('licenses/import', views.import_data, name='licenses_import'),

    path('licenses_type/list', views.LicenseTypeListView.as_view(), name='licenses_type_list'),
    path('licenses_type/create', views.LicenseTypeCreateView.as_view(), name='licenses_type_create'),
    path('licenses_type/<int:pk>/update', views.LicenseTypeUpdateView.as_view(), name='licenses_type_update'),
    path('licenses_type/<int:pk>/delete', views.LicenseTypeDeleteView.as_view(), name='licenses_type_delete'),
]