from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from licenses.models import License, LicensesInventory

def license_inventory_update():
    licenses_count = License.objects.all().count()
    licenses_value = License.objects.aggregate(
        total_value = Sum('value')
    ) ['total_value']

    LicensesInventory.objects.create(
        licenses_count = licenses_count,
        licenses_value = licenses_value
    )


@receiver(post_save, sender=License)
def license_post_save(sender, instance, **kwargs):
    license_inventory_update()

@receiver(post_delete, sender=License)
def license_post_delete(sender, instance, **kwargs):
    license_inventory_update()
