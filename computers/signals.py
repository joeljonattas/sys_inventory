from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from computers.models import Computer, ComputersInventory

def computer_inventory_update():
    computers_count = Computer.objects.all().count()
    computers_value = Computer.objects.aggregate(
        total_value = Sum('value')
    ) ['total_value']

    ComputersInventory.objects.create(
        computers_count = computers_count,
        computers_value = computers_value
    )


@receiver(post_save, sender=Computer)
def computer_post_save(sender, instance, **kwargs):
    computer_inventory_update()

@receiver(post_delete, sender=Computer)
def computer_post_delete(sender, instance, **kwargs):
    computer_inventory_update()
