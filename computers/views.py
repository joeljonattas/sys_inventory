from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models
from brands.models import Brand
from categories.models import Category
from . import forms
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from tablib import Dataset
from app.resources import ComputerResource, ComputerImportResource
from app.files import remove_styles_from_xlsx
from django.contrib.contenttypes.models import ContentType
from auditlog.models import LogEntry


# Create your views here.
class ComputersListView(LoginRequiredMixin, ListView):
    model = models.Computer
    template_name = 'computers_list.html'
    context_object_name = 'computers'
    paginate_by = 9

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

        if category:
            queryset = queryset.filter(category__id=category)

        if stat:
            queryset = queryset.filter(status=stat)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        context['status'] = models.Computer.STATUS_CHOICES
        return context

    
class ComputersCreateView(LoginRequiredMixin, CreateView):
    model = models.Computer
    template_name = 'computers_create.html'
    success_url = reverse_lazy('computers_list')
    form_class = forms.ComputersForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class ComputersDetailView(LoginRequiredMixin, DetailView):
    model = models.Computer
    template_name = 'computers_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        computer_content_type = ContentType.objects.get_for_model(models.Computer)

        logs = LogEntry.objects.filter(
            content_type=computer_content_type,
            object_id=self.object.id
        )
        
        context['logs'] = logs

        return context

class ComputersUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Computer
    template_name = 'computers_update.html'
    form_class = forms.ComputersForm
    success_url = reverse_lazy('computers_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class ComputersDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Computer
    template_name = 'computers_delete.html'
    success_url = reverse_lazy('computers_list')

def qr_code_view(request, pk):
    object = get_object_or_404(models.Computer, pk=pk)
    return render(request, 'qr_code.html', {'object': object})

# Exportação
def export_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        status_id = request.POST.get('stat')
        category_id = request.POST.get('category')
        computer_resource = ComputerResource()

        if status_id:
            computer_filter = models.Computer.objects.filter(status__id=status_id)
        elif category_id:
            computer_filter = models.Computer.objects.filter(category__id=category_id)
        else:
            computer_filter = models.Computer.objects.all()

        dataset = computer_resource.export(computer_filter)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="computers_data.csv"'
            return response        
        elif file_format == 'XLSX (Excel)':
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="computers_data.xlsx"'
            return response  

    return redirect('computers_list')

# Importação
def import_data(request):
    if request.method == 'POST':
        try:
            file_format = request.POST['file-format']
            computers_resource = ComputerImportResource()
            dataset = Dataset()
            new_computers = request.FILES['importData']

            if file_format == 'CSV':
                dataset = dataset.load(new_computers.read().decode('utf-8'), format='csv')

            if file_format == 'XLSX':
                cleaned_file = remove_styles_from_xlsx(new_computers)
                dataset = Dataset().load(cleaned_file.read(), format='xlsx')

            result = computers_resource.import_data(dataset, dry_run=True, raise_errors=True)

            if result.has_errors():
                for error in result.row_errors():
                    messages.error(
                        request,
                        f"Erro na linha {error}."
                    )
            else:
                computers_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Importação realizada com sucesso.")

        except Exception as e:
            messages.error(request, f"Erro durante o processo de importação: {e}")

    return redirect('computers_list')