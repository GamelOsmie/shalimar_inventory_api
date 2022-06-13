from django.contrib import admin
from .models import Shipment, CommercialInvoice, ProformaInvoice, Container, WarehouseSparePartsSupply, WarehouseVehiclesSupply

# Register your models here.
admin.site.register(Shipment)
admin.site.register(CommercialInvoice)
admin.site.register(ProformaInvoice)
admin.site.register(Container)
admin.site.register(WarehouseVehiclesSupply)
admin.site.register(WarehouseSparePartsSupply)
