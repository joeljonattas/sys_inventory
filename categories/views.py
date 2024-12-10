from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models
from . import forms
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect


class CategoriesListView(LoginRequiredMixin, ListView):
    model = models.Category
    template_name = 'categories_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        
        return queryset


class CategoriesCreateView(LoginRequiredMixin, CreateView):
    model = models.Category
    template_name = 'categories_create.html'
    success_url = reverse_lazy('categories_list')
    form_class = forms.CategoriesForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)


class CategoriesUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Category
    template_name = 'categories_update.html'
    form_class = forms.CategoriesForm
    success_url = reverse_lazy('categories_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)


class CategoriesDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Category
    template_name = 'categories_delete.html'
    success_url = reverse_lazy('categories_list')


 
