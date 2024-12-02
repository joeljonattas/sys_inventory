from django.urls import path
from . import views

urlpatterns = [
    path('brands/list', views.BrandsListView.as_view(), name='brands_list'),
    path('brands/create', views.BrandsCreateView.as_view(), name='brands_create'),
    path('brands/<int:pk>/update', views.BrandsUpdateView.as_view(), name='brands_update'),
    path('brands/<int:pk>/delete', views.BrandsDeleteView.as_view(), name='brands_delete'),
]