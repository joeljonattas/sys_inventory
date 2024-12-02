from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from .models import Phone, PhonesInventory, PhoneNumber, PhonesNumberInventory

def phones_update_inventory():
    phones_count = Phone.objects.all().count()
    phones_value = Phone.objects.aggregate(
        total_value = Sum('value')
    ) ['total_value']

    PhonesInventory.objects.create(
        phones_count = phones_count,
        phones_value = phones_value
    )

def phones_line_update_inventory():
    phones_line_count = PhoneNumber.objects.all().count()
    phones_line_value = PhoneNumber.objects.aggregate(
        total_value = Sum('value')
    ) ['total_value']

    PhonesNumberInventory.objects.create(
        phones_line_count = phones_line_count,
        phones_line_value = phones_line_value
    )

@receiver(post_save, sender=Phone)
def phones_post_save(sender, instance, **kwargs):
    phones_update_inventory()

@receiver(post_delete, sender=Phone)
def phones_post_delete(sender, instance, **kwargs):
    phones_update_inventory()

@receiver(post_save, sender=PhoneNumber)
def phones_post_save(sender, instance, **kwargs):
    phones_line_update_inventory()

@receiver(post_delete, sender=PhoneNumber)
def phones_post_delete(sender, instance, **kwargs):
    phones_line_update_inventory()

