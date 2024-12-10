from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import License, LicenseType
from .forms import LicensesForm, LicenseTypeForm
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from auditlog.models import LogEntry
from app.resources import LicenseResource, LicenseImportResource
from django.contrib import messages
from django.http import HttpResponse
from tablib import Dataset
from app.files import remove_styles_from_xlsx
from django.shortcuts import redirect

# Create your views here.
class LicenseListView(LoginRequiredMixin, ListView):
    model = License
    template_name = './licenses/licenses_list.html'
    context_object_name = 'licenses'

    def get_queryset(self):
        queryset = super().get_queryset()
        stat = self.request.GET.get('stat')
        software_filter = self.request.GET.get('software')
        license_type = self.request.GET.get('license_type')

        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(license_key=search_query)
            )

        if stat:
            queryset = queryset.filter(status=stat)

        if software_filter:
            queryset = queryset.filter(software=software_filter)

        if license_type:
            queryset = queryset.filter(license_type=license_type)
            
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = License.STATUS_CHOICES
        context['softwares'] = License.SOFTWARE_CHOICES
        context['licenses_types'] = LicenseType.objects.all()

        return context

class LicenseCreateView(LoginRequiredMixin, CreateView):
    model = License
    template_name = './licenses/licenses_create.html'
    success_url = reverse_lazy('licenses_list')
    form_class = LicensesForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class LicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = License
    template_name = './licenses/licenses_update.html'
    success_url = reverse_lazy('licenses_list')
    form_class = LicensesForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class LicenseDetailView(LoginRequiredMixin, DetailView):
    model = License
    template_name = './licenses/licenses_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_content_type = ContentType.objects.get_for_model(License)

        logs = LogEntry.objects.filter(
            content_type=license_content_type,
            object_id=self.object.id
        )
        
        context['logs'] = logs

        return context

class LicenseDeleteView(LoginRequiredMixin, DeleteView):
    model = License
    template_name = './licenses/licenses_delete.html'
    success_url = reverse_lazy('licenses_list')

# Exportação
def export_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        status = request.POST.get('stat')
        software = request.POST.get('software')
        licenses_resource = LicenseResource()

        if status:
            license_filter = License.objects.filter(status=status)
        elif software:
            license_filter = License.objects.filter(software=software)
        else:
            license_filter = License.objects.all()


        dataset = licenses_resource.export(license_filter)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="licenses_data.csv"'
            return response        
        elif file_format == 'XLSX (Excel)':
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="licenses_data.xlsx"'
            return response

    return redirect('licenses_list')

# Importação
def import_data(request):
    if request.method == 'POST':
        try:
            file_format = request.POST['file-format']
            licenses_resource = LicenseImportResource()
            dataset = Dataset()
            new_licenses = request.FILES['importData']

            if file_format == 'CSV':
                dataset = dataset.load(new_licenses.read().decode('utf-8'), format='csv')

            if file_format == 'XLSX':
                cleaned_file = remove_styles_from_xlsx(new_licenses)
                dataset = Dataset().load(cleaned_file.read(), format='xlsx')

            result = licenses_resource.import_data(dataset, dry_run=True, raise_errors=True)

            if result.has_errors():
                for error in result.row_errors():
                    messages.error(
                        request,
                        f"Erro na linha {error}."
                    )
            else:
                licenses_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Importação realizada com sucesso.")

        except Exception as e:
            messages.error(request, f"Erro durante o processo de importação: {e}")

    return redirect('licenses_list')



# LicenseType
class LicenseTypeListView(LoginRequiredMixin, ListView):
    model = LicenseType
    template_name = './licenses_type/licenses_type_list.html'
    context_object_name = 'licenses_type'

class LicenseTypeCreateView(LoginRequiredMixin, CreateView):
    model = LicenseType
    template_name = './licenses_type/licenses_type_create.html'
    success_url = reverse_lazy('licenses_type_list')
    form_class = LicenseTypeForm

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class LicenseTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = LicenseType
    template_name = './licenses_type/licenses_type_update.html'
    success_url = reverse_lazy('licenses_type_list')
    form_class = LicenseTypeForm

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class LicenseTypeDetailView(LoginRequiredMixin, DetailView):
    model = LicenseType
    template_name = './licenses_type/licenses_type_detail.html'

class LicenseTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = LicenseType
    template_name = './licenses_type/licenses_type_delete.html'
    success_url = reverse_lazy('licenses_type_list')