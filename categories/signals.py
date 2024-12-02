from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from computers.models import Computer
from printers.models import Printer
from licenses.models import License
from phones.models import Phone

@receiver(pre_save, sender=Computer)
@receiver(pre_save, sender=Printer)
@receiver(pre_save, sender=Phone)
@receiver(pre_save, sender=License)
def save_old_category(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_category = sender.objects.get(pk=instance.pk).category
        except sender.DoesNotExist:
            instance._old_category = None
    else:
        instance._old_category = None

def update_category_count(category):
    if category:
        category.equipament_count = (
            Computer.objects.filter(category=category).count()+
            Phone.objects.filter(category=category).count()+
            Printer.objects.filter(category=category).count()+
            License.objects.filter(category=category).count()
        )

        category.save()

@receiver(post_save, sender=Computer)
@receiver(post_save, sender=Printer)
@receiver(post_save, sender=Phone)
@receiver(post_save, sender=License)
def update_category_count_post_save(sender, instance, **kwargs):
    update_category_count(instance.category)

    if hasattr(instance, '_old_category') and instance._old_category != instance.category:
        update_category_count(instance._old_category)

@receiver(post_delete, sender=Computer)
@receiver(post_delete, sender=Printer)
@receiver(post_delete, sender=Phone)
@receiver(post_delete, sender=License)
def update_category_count_post_delete(sender, instance, **kwargs):
    update_category_count(instance.category)