from typing import Any
from django.urls import reverse_lazy
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models
from .models import PhoneNumber, Phone, PhoneOperator
from brands.models import Brand
from categories.models import Category
from . import forms
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from app.files import remove_styles_from_xlsx
from django.contrib import messages
from django.http import HttpResponse
from tablib import Dataset
from app.resources import PhoneResource, PhoneNumberResource, PhoneImportResource, PhoneNumberImportResource
from django.contrib.contenttypes.models import ContentType
from auditlog.models import LogEntry
from django.db.models import ProtectedError

# Create your views here.
class PhonesListView(LoginRequiredMixin, ListView):
    model = Phone
    template_name = './phones/phones_list.html'
    context_object_name = 'phones'

    def get_queryset(self):
        queryset = super().get_queryset()
        brand = self.request.GET.get('brand')
        category = self.request.GET.get('category')
        stat = self.request.GET.get('stat')
        
        # Obtendo o termo de busca
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(model__icontains=search_query) | Q(serie_number__icontains=search_query) | Q(name__icontains=search_query)
            )

        if brand:
            queryset = queryset.filter(brand__id=brand)

        if stat:
            queryset = queryset.filter(status=stat)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        context['status'] = Phone.STATUS_CHOICES
        return context
    
class PhonesCreateView(LoginRequiredMixin, CreateView):
    model = Phone
    template_name = './phones/phones_create.html'
    success_url = reverse_lazy('phones_list')
    form_class = forms.PhonesForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['numbers'] = PhoneNumber.objects.filter(phone_number__isnull=True)
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class PhonesDetailView(LoginRequiredMixin, DetailView):
    model = Phone
    template_name = './phones/phones_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        computer_content_type = ContentType.objects.get_for_model(models.Phone)

        logs = LogEntry.objects.filter(
            content_type=computer_content_type,
            object_id=self.object.id
        )
        
        context['logs'] = logs

        return context

class PhonesUpdateView(LoginRequiredMixin, UpdateView):
    model = Phone
    template_name = './phones/phones_update.html'
    form_class = forms.PhonesForm
    success_url = reverse_lazy('phones_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        phone = self.get_object()

        kwargs['numbers'] = PhoneNumber.objects.filter(
            Q(phone_number__isnull=True) | Q(id=phone.number_id)
        )
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class PhonesDeleteView(LoginRequiredMixin, DeleteView):
    model = Phone
    template_name = './phones/phones_delete.html'
    success_url = reverse_lazy('phones_list')

def qr_code_view(request, pk):
    object = get_object_or_404(Phone, pk=pk)
    return render(request, './phones/qr_code_phones.html', {'object': object})

# Exportação
def export_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        status_id = request.POST.get('stat')
        category_id = request.POST.get('category')
        phone_resource = PhoneResource()

        if status_id:
            phone_filter = Phone.objects.filter(status__id=status_id)
        elif category_id:
            phone_filter = Phone.objects.filter(category__id=category_id)
        else:
            phone_filter = Phone.objects.all()


        dataset = phone_resource.export(phone_filter)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="phone_data.csv"'
            return response        
        elif file_format == 'XLSX (Excel)':
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="phone_data.xlsx"'
            return response  

    return redirect('phones_list')

# Importação
def import_data(request):
    if request.method == 'POST':
        try:
            file_format = request.POST['file-format']
            phone_resource = PhoneImportResource()
            dataset = Dataset()
            new_phones = request.FILES['importData']

            if file_format == 'CSV':
                dataset = dataset.load(new_phones.read().decode('utf-8'), format='csv')

            if file_format == 'XLSX':
                cleaned_file = remove_styles_from_xlsx(new_phones)
                dataset = Dataset().load(cleaned_file.read(), format='xlsx')

            result = phone_resource.import_data(dataset, dry_run=True, raise_errors=True)

            if result.has_errors():
                for error in result.row_errors():
                    messages.error(
                        request,
                        f"Erro na linha {error}."
                    )
            else:
                phone_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Importação realizada com sucesso.")

        except Exception as e:
            messages.error(request, f"Erro durante o processo de importação: {e}")

    return redirect('phones_list')


# Lines
class PhonesLinesListView(LoginRequiredMixin, ListView):
    model = models.PhoneNumber
    template_name = './phones_lines/phones_lines_list.html'
    context_object_name = 'phones_lines'

    def get_queryset(self):
        queryset = super().get_queryset()
        stat = self.request.GET.get('stat')
        operator = self.request.GET.get('operator')
        
        # Obtendo o termo de busca
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(number__icontains=search_query) | Q(name__icontains=search_query)
            )

        if stat:
            queryset = queryset.filter(status=stat)

        if operator:
            queryset = queryset.filter(operator__id=operator)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operators'] = models.PhoneOperator.objects.all()
        context['status'] = PhoneNumber.STATUS_CHOICES
        return context

class PhonesLinesCreateView(LoginRequiredMixin, CreateView):
    model = models.PhoneNumber
    template_name = './phones_lines/phones_lines_create.html'
    success_url = reverse_lazy('phones_lines_list')
    form_class = forms.PhonesLinesForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class PhonesLinesDetailView(LoginRequiredMixin, DetailView):
    model = models.PhoneNumber
    template_name = './phones_lines/phones_lines_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        computer_content_type = ContentType.objects.get_for_model(models.PhoneNumber)

        logs = LogEntry.objects.filter(
            content_type=computer_content_type,
            object_id=self.object.id
        )
        
        context['logs'] = logs

        return context

class PhonesLinesUpdateView(LoginRequiredMixin, UpdateView):
    model = models.PhoneNumber
    template_name = './phones_lines/phones_lines_update.html'
    form_class = forms.PhonesLinesForm
    success_url = reverse_lazy('phones_lines_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class PhonesLinesDeleteView(LoginRequiredMixin, DeleteView):
    model = models.PhoneNumber
    template_name = './phones_lines/phones_lines_delete.html'
    success_url = reverse_lazy('phones_lines_list')


# Exportação
def export_data_phone_lines(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        status_id = request.POST.get('stat')
        operator_id = request.POST.get('operator')
        phone_line_resource = PhoneNumberResource()

        if status_id:
            phone_line_filter = models.PhoneNumber.objects.filter(status__id=status_id)
        elif operator_id:
            phone_line_filter = models.PhoneNumber.objects.filter(operator__id=operator_id)
        else:
            phone_line_filter = models.PhoneNumber.objects.all()


        dataset = phone_line_resource.export(phone_line_filter)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="phone_line_data.csv"'
            return response        
        elif file_format == 'XLSX (Excel)':
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="phone_line_data.xlsx"'
            return response  
        
    return redirect('phones_lines_list')

# Importação
def import_data_phone_lines(request):
    if request.method == 'POST':
        try:
            file_format = request.POST['file-format']
            phone_line_resource = PhoneNumberImportResource()
            dataset = Dataset()
            new_phones_lines = request.FILES['importData']

            if file_format == 'CSV':
                dataset = dataset.load(new_phones_lines.read().decode('utf-8'), format='csv')

            if file_format == 'XLSX':
                cleaned_file = remove_styles_from_xlsx(new_phones_lines)
                dataset = Dataset().load(cleaned_file.read(), format='xlsx')

            result = phone_line_resource.import_data(dataset, dry_run=True, raise_errors=True)

            if result.has_errors():
                for error in result.row_errors():
                    messages.error(
                        request,
                        f"Erro na linha {error}."
                    )
            else:
                phone_line_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Importação realizada com sucesso.")

        except Exception as e:
            messages.error(request, f"Erro durante o processo de importação: {e}")

    return redirect('phones_lines_list')

# Operators
class PhoneOperatorListView(LoginRequiredMixin, ListView):
    model = PhoneOperator
    template_name = './operators/operators_list.html'
    context_object_name = 'operators'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Obtendo o termo de busca
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )

        
        return queryset

class PhoneOperatorCreateView(LoginRequiredMixin, CreateView):
    model = PhoneOperator
    template_name = './operators/operators_create.html'
    success_url = reverse_lazy('operators_list')
    form_class = forms.OperatorsForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class PhoneOperatorUpdateView(LoginRequiredMixin, UpdateView):
    model = PhoneOperator
    template_name = './operators/operators_update.html'
    form_class = forms.OperatorsForm
    success_url = reverse_lazy('operators_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class PhoneOperatorDeleteView(LoginRequiredMixin, DeleteView):
    model = PhoneOperator
    template_name = './operators/operators_delete.html'
    success_url = reverse_lazy('operators_list')