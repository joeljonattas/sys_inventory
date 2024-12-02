from django.urls import reverse_lazy
from django.http import HttpResponse
from tablib import Dataset
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Collaborator
from .models import Sector
from computers.models import Computer
from phones.models import Phone, PhoneNumber
from . import forms
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from app.resources import CollaboratorResource, CollaboratorImportResource
from django.contrib import messages
from app.files import remove_styles_from_xlsx
from django.contrib.contenttypes.models import ContentType
from auditlog.models import LogEntry

class CollaboratorsListView(LoginRequiredMixin, ListView):
    model = Collaborator
    template_name = 'collaborators_list.html'
    context_object_name = 'collaborators'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        sector = self.request.GET.get('sector')
        
        # Obtendo o termo de busca
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(email__icontains=search_query)
            )

        if sector:
            queryset = queryset.filter(sector__id=sector)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sectors'] = Sector.objects.all()
        return context


class CollaboratorsCreateView(LoginRequiredMixin, CreateView):
    model = Collaborator
    template_name = 'collaborators_create.html'
    success_url = reverse_lazy('collaborators_list')
    form_class = forms.CollaboratorsForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['computers'] = Computer.objects.filter(status='in_stock').exclude(category__name='Servidor')
        kwargs['phones'] = Phone.objects.filter(status='in_stock')
        kwargs['phone_numbers'] = PhoneNumber.objects.filter(status='in_stock')
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)


class CollaboratorsDetailView(LoginRequiredMixin, DetailView):
    model = Collaborator
    template_name = 'collaborators_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        collaborator_content_type = ContentType.objects.get_for_model(Collaborator)

        logs = LogEntry.objects.filter(
            content_type=collaborator_content_type,
            object_id=self.object.id
        )

        context['logs'] = logs

        return context


class CollaboratorsUpdateView(LoginRequiredMixin, UpdateView):
    model = Collaborator
    template_name = 'collaborators_update.html'
    form_class = forms.CollaboratorsForm
    success_url = reverse_lazy('collaborators_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        collaborator = self.get_object()

        kwargs['computers'] = Computer.objects.filter(
            Q(collaborator_computer__isnull=True) | Q(id=collaborator.computer_id)
        ).exclude(category__name='Servidor')
        kwargs['phones'] = Phone.objects.filter(
            Q(collaborator_phone__isnull=True) | Q(id=collaborator.phone_id)
        )
        kwargs['phone_numbers'] = PhoneNumber.objects.filter(
            Q(collaborator_number__isnull=True) | Q(id=collaborator.phone_number_id)
        )
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)


class CollaboratorsDeleteView(LoginRequiredMixin, DeleteView):
    model = Collaborator
    template_name = 'collaborators_delete.html'
    success_url = reverse_lazy('collaborators_list')

# Sectors
class SectorsListView(LoginRequiredMixin, ListView):
    model = Sector
    template_name = './sectors/sectors_list.html'
    context_object_name = 'sectors'
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


class SectorsCreateView(LoginRequiredMixin, CreateView):
    model = Sector
    template_name = './sectors/sectors_create.html'
    success_url = reverse_lazy('sectors_list')
    form_class = forms.SectorsForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)


class SectorsDetailView(LoginRequiredMixin, DetailView):
    model = Sector
    template_name = './sectors/sectors_detail.html'


class SectorsUpdateView(LoginRequiredMixin, UpdateView):
    model = Sector
    template_name = './sectors/sectors_update.html'
    form_class = forms.SectorsForm
    success_url = reverse_lazy('sectors_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)


class SectorsDeleteView(LoginRequiredMixin, DeleteView):
    model = Sector
    template_name = './sectors/sectors_delete.html'
    success_url = reverse_lazy('sectors_list')


def export_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        sector_id = request.POST.get('sector')
        category_resource = CollaboratorResource()
        obj = 'collaborator'

        if sector_id:
            collaborators_sector = Collaborator.objects.filter(sector__id=sector_id)
        else:
            collaborators_sector = Collaborator.objects.all()

        dataset = category_resource.export(collaborators_sector)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="collaborators_data.csv"'
            return response        
        elif file_format == 'XLSX (Excel)':
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="collaborators_data.xlsx"'
            return response  

    return redirect('collaborators_list')

# Importação
def import_data(request):
    if request.method == 'POST':
        try:
            file_format = request.POST['file-format']
            collaborators_resource = CollaboratorImportResource()
            dataset = Dataset()
            new_collaborators = request.FILES['importData']

            if file_format == 'CSV':
                dataset = dataset.load(new_collaborators.read().decode('utf-8'), format='csv')

            if file_format == 'XLSX':
                cleaned_file = remove_styles_from_xlsx(new_collaborators)
                dataset = Dataset().load(cleaned_file.read(), format='xlsx')

            result = collaborators_resource.import_data(dataset, dry_run=True, raise_errors=True)

            if result.has_errors():
                for error in result.row_errors():
                    print(error)
                    line_number = error[0]
                    row_data = error[1].values if error[1] else "Linha desconhecida"
                    messages.error(
                        request,
                        f"Erro na linha {line_number}: {error[1]}. Dados: {row_data}"
                    )
            else:
                collaborators_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Importação realizada com sucesso.")

        except Exception as e:
            messages.error(request, f"Erro durante o processo de importação: {e}")
            print(e)

    return redirect('collaborators_list')