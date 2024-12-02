from django.urls import path
from . import views

urlpatterns = [
    path('phones/list', views.PhonesListView.as_view(), name='phones_list'),
    path('phones/create', views.PhonesCreateView.as_view(), name='phones_create'),
    path('phones/<int:pk>/detail', views.PhonesDetailView.as_view(), name='phones_detail'),
    path('phones/<int:pk>/update', views.PhonesUpdateView.as_view(), name='phones_update'),
    path('phones/<int:pk>/delete', views.PhonesDeleteView.as_view(), name='phones_delete'),
    path('phones/export', views.export_data, name='phones_export'),
    path('phones/import', views.import_data, name='phones_import'),
    path('phones/<int:pk>/qr_code', views.qr_code_view, name='phones_qr_code'),

    path('phones_lines/list', views.PhonesLinesListView.as_view(), name='phones_lines_list'),
    path('phones_lines/create', views.PhonesLinesCreateView.as_view(), name='phones_lines_create'),
    path('phones_lines/<int:pk>/detail', views.PhonesLinesDetailView.as_view(), name='phones_lines_detail'),
    path('phones_lines/<int:pk>/update', views.PhonesLinesUpdateView.as_view(), name='phones_lines_update'),
    path('phones_lines/<int:pk>/delete', views.PhonesLinesDeleteView.as_view(), name='phones_lines_delete'),
    path('phones_lines/export', views.export_data_phone_lines, name='phones_lines_export'),
    path('phones_lines/import', views.import_data_phone_lines, name='phones_lines_import'),

    path('operators/list', views.PhoneOperatorListView.as_view(), name='operators_list'),
    path('operators/create', views.PhoneOperatorCreateView.as_view(), name='operators_create'),
    path('operators/<int:pk>/update', views.PhoneOperatorUpdateView.as_view(), name='operators_update'),
    path('operators/<int:pk>/delete', views.PhoneOperatorDeleteView.as_view(), name='operators_delete'),
]    