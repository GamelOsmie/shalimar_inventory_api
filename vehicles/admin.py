from django.contrib import admin
from .models import SparePart, Tax, Vehicle

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(SparePart)
admin.site.register(Tax)