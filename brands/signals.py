from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from computers.models import Computer
from printers.models import Printer
from phones.models import Phone

@receiver(pre_save, sender=Computer)
@receiver(pre_save, sender=Printer)
@receiver(pre_save, sender=Phone)
def save_old_brand(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_brand = sender.objects.get(pk=instance.pk).brand
        except sender.DoesNotExist:
            instance._old_brand = None
    else:
        instance._old_brand = None

def update_brand_count(brand):
    if brand:
        brand.equipament_count = (
            Computer.objects.filter(brand=brand).count()+
            Phone.objects.filter(brand=brand).count()+
            Printer.objects.filter(brand=brand).count()
        )

        brand.save()

@receiver(post_save, sender=Computer)
@receiver(post_save, sender=Printer)
@receiver(post_save, sender=Phone)
def update_brand_count_post_save(sender, instance, **kwargs):
    update_brand_count(instance.brand)

    if hasattr(instance, '_old_brand') and instance._old_brand != instance.brand:
        update_brand_count(instance._old_brand)

@receiver(post_delete, sender=Computer)
@receiver(post_delete, sender=Printer)
@receiver(post_delete, sender=Phone)
def update_brand_count_post_delete(sender, instance, **kwargs):
    update_brand_count(instance.brand)