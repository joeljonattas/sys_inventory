from django.urls import path
from . import views

urlpatterns = [
    path('categories/list', views.CategoriesListView.as_view(), name='categories_list'),
    path('categories/create', views.CategoriesCreateView.as_view(), name='categories_create'),
    path('categories/<int:pk>/update', views.CategoriesUpdateView.as_view(), name='categories_update'),
    path('categories/<int:pk>/delete', views.CategoriesDeleteView.as_view(), name='categories_delete'),
]