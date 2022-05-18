from operations.models import WarehouseOperation, ServiceShopOperation, BranchOperation
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Branch)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        BranchOperation.objects.create(branch=instance)


@receiver(post_save, sender=Warehouse)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        WarehouseOperation.objects.create(warehouse=instance)


@receiver(post_save, sender=ServiceShop)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        ServiceShopOperation.objects.create(service_shop=instance)
