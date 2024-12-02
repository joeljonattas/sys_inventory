from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from printers.models import Printer, PrintersInventory

def printer_inventory_update():
    printers_count = Printer.objects.all().count()
    printers_value = Printer.objects.aggregate(
        total_value = Sum('value')
    ) ['total_value']

    PrintersInventory.objects.create(
        printers_count = printers_count,
        printers_value = printers_value
    )


@receiver(post_save, sender=Printer)
def printer_post_save(sender, instance, **kwargs):
    printer_inventory_update()

@receiver(post_delete, sender=Printer)
def printer_post_delete(sender, instance, **kwargs):
    printer_inventory_update()
