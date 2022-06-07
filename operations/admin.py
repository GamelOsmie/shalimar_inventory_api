from django.contrib import admin
from .models import Shipment, CommercialInvoice, ProformaInvoice, Container

# Register your models here.
admin.site.register(Shipment)
admin.site.register(CommercialInvoice)
admin.site.register(ProformaInvoice)
admin.site.register(Container)
