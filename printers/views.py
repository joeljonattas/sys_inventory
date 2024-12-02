from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Printer
from django.contrib.contenttypes.models import ContentType
from auditlog.models import LogEntry
from .forms import PrintersForm
from brands.models import Brand
from categories.models import Category
from collaborators.models import Sector
from app.resources import PrinterResource, PrinterImportResource
from django.contrib import messages
from django.http import HttpResponse
from tablib import Dataset
from app.files import remove_styles_from_xlsx
from django.contrib import messages

# Create your views here.
class PrintersListView(LoginRequiredMixin, ListView):
    model = Printer
    template_name = 'printers_list.html'
    context_object_name = 'printers'

    def get_queryset(self):
        queryset = super().get_queryset()
        brand = self.request.GET.get('brand')
        location = self.request.GET.get('location')
        stat = self.request.GET.get('stat')

        # Obtendo o termo de busca
        search_query = self.request.GET.get('search')
        
        if search_query:
            queryset = queryset.filter(
                Q(model__icontains=search_query) | Q(serie_number__icontains=search_query) | Q(name__icontains=search_query)
            )

        if brand:
            queryset = queryset.filter(brand__id=brand)

        if location:
            queryset = queryset.filter(location__id=location)

        if stat:
            queryset = queryset.filter(status=stat)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['locations'] = Sector.objects.all()
        context['status'] = Printer.STATUS_CHOICES
        return context

class PrintersCreateView(LoginRequiredMixin, CreateView):
    model = Printer
    template_name = 'printers_create.html'
    form_class = PrintersForm
    success_url = reverse_lazy('printers_list')

    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao cadastrar. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class PrintersUpdateView(LoginRequiredMixin, UpdateView):
    model = Printer
    template_name = 'printers_update.html'
    form_class = PrintersForm
    success_url = reverse_lazy('printers_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao atualizar dados. Verifique os dados e tente novamente.")
        return super().form_invalid(form)

class PrintersDetailView(LoginRequiredMixin, DetailView):
    model = Printer
    template_name = 'printers_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        license_content_type = ContentType.objects.get_for_model(Printer)

        logs = LogEntry.objects.filter(
            content_type=license_content_type,
            object_id=self.object.id
        )
        
        context['logs'] = logs

        return context
    
class PrintersDeleteView(LoginRequiredMixin, DeleteView):
    model = Printer
    template_name = 'printers_delete.html'
    success_url = reverse_lazy('printers_list')

def qr_code_view(request, pk):
    object = get_object_or_404(Printer, pk=pk)
    return render(request, 'qr_code_printer.html', {'object': object})

# Exportação
def export_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        status = request.POST.get('stat')
        category_id = request.POST.get('category')
        computer_resource = PrinterResource()

        if status:
            printer_filter = Printer.objects.filter(status=status)
        elif category_id:
            printer_filter = Printer.objects.filter(category__id=category_id)
        else:
            printer_filter = Printer.objects.all()

        dataset = computer_resource.export(printer_filter)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="printers_data.csv"'
            return response        
        elif file_format == 'XLSX (Excel)':
            response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="printers_data.xlsx"'
            return response  

    return redirect('printers_list')

# Importação
def import_data(request):
    if request.method == 'POST':
        try:
            file_format = request.POST['file-format']
            printer_resource = PrinterImportResource()
            dataset = Dataset()
            new_printers = request.FILES['importData']

            if file_format == 'CSV':
                dataset = dataset.load(new_printers.read().decode('utf-8'), format='csv')
            elif file_format == 'XLSX':
                cleaned_file = remove_styles_from_xlsx(new_printers)
                dataset = Dataset().load(cleaned_file.read(), format='xlsx')

            result = printer_resource.import_data(dataset, dry_run=True, raise_errors=True)

            if result.has_errors():
                for error in result.row_errors():
                    print(error)
                    line_number = error[0]
                    row_data = error[1].values if error[1] else "Linha desconhecida"
                    messages.error(
                        request,
                        f"Erro na linha {line_number}: {error[1]}."
                    )
            else:
                printer_resource.import_data(dataset, dry_run=False)
                messages.success(request, "Importação realizada com sucesso.")

        except Exception as e:
            messages.error(request, f"Erro durante o processo de importação: {e}")
            print(e)

    return redirect('printers_list')