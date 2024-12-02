from django.urls import path
from . import views

urlpatterns = [
    path('collaborators/list', views.CollaboratorsListView.as_view(), name='collaborators_list'),
    path('collaborators/create', views.CollaboratorsCreateView.as_view(), name='collaborators_create'),
    path('collaborators/<int:pk>/detail', views.CollaboratorsDetailView.as_view(), name='collaborators_detail'),
    path('collaborators/<int:pk>/update', views.CollaboratorsUpdateView.as_view(), name='collaborators_update'),
    path('collaborators/<int:pk>/delete', views.CollaboratorsDeleteView.as_view(), name='collaborators_delete'),
    path('collaborators/export', views.export_data, name='collaborators_export'),
    path('collaborators/import', views.import_data, name='collaborators_import'),

    path('sectors/list', views.SectorsListView.as_view(), name='sectors_list'),
    path('sectors/create', views.SectorsCreateView.as_view(), name='sectors_create'),
    path('sectors/<int:pk>/detail', views.SectorsDetailView.as_view(), name='sectors_detail'),
    path('sectors/<int:pk>/update', views.SectorsUpdateView.as_view(), name='sectors_update'),
    path('sectors/<int:pk>/delete', views.SectorsDeleteView.as_view(), name='sectors_delete'),
]