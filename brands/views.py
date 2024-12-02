from typing import Any
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models
from . import forms
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class BrandsListView(LoginRequiredMixin, ListView):
    model = models.Brand
    template_name = 'brands_list.html'
    context_object_name = 'brands'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Obtendo o termo de busca
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        
        return queryset


class BrandsCreateView(LoginRequiredMixin, CreateView):
    model = models.Brand
    template_name = 'brands_create.html'
    success_url = reverse_lazy('brands_list')
    form_class = forms.BrandsForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)



class BrandsUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Brand
    template_name = 'brands_update.html'
    form_class = forms.BrandsForm
    success_url = reverse_lazy('brands_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)


class BrandsDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Brand
    template_name = 'brands_delete.html'
    success_url = reverse_lazy('brands_list')
