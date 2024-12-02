from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from .models import Collaborator
from computers.models import Computer
from phones.models import Phone, PhoneNumber

@receiver(pre_save, sender=Collaborator)
def capture_previous_equipament(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Collaborator.objects.get(pk=instance.pk)
            instance._previous_computer = old_instance.computer
            instance._previous_phone = old_instance.phone
            instance._previous_phone_number = old_instance.phone_number
        except Collaborator.DoesNotExist:
            instance._previous_computer = None
            instance._previous_phone = None
            instance._previous_phone_number = None

@receiver(post_save, sender=Collaborator)
def update_status_equipament(sender, instance, **kwargs):
    active_status = 'active'
    in_stock_status = 'in_stock'

    if instance.computer:
        instance.computer.status = active_status
        instance.computer.save()

    if hasattr(instance, '_previous_computer'):
        previous_computer = instance._previous_computer
        if previous_computer and previous_computer != instance.computer:
            previous_computer.status = in_stock_status
            previous_computer.save()

    if instance.phone:
        instance.phone.status = active_status
        instance.phone.number = instance.phone_number
        instance.phone.save()

    if hasattr(instance, '_previous_phone'):
        previous_phone = instance._previous_phone
        if previous_phone and previous_phone != instance.phone:
            previous_phone.status = in_stock_status
            previous_phone.number = None
            previous_phone.save()

    if instance.phone_number:
        instance.phone_number.status = active_status
        instance.phone_number.save()

    if hasattr(instance, '_previous_phone_number'):
        previous_phone_number = instance._previous_phone_number
        if previous_phone_number and previous_phone_number != instance.phone_number:
            previous_phone_number.status = in_stock_status
            previous_phone_number.save()


@receiver(post_delete, sender=Collaborator)
def update_status_equipament_post_delete(sender, instance, **kwargs):
    in_stock_status = 'in_stock'

    if instance.computer:
        instance.computer.status = in_stock_status
        instance.computer.save()

    if instance.phone:
        instance.phone.status = in_stock_status
        instance.phone.save()

    if instance.phone_number:
        instance.phone_number.status = in_stock_status
        instance.phone_number.save()
