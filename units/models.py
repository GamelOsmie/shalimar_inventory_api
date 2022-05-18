from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.functions import Lower
import uuid

# Create your models here.
class Branch(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, blank=False, unique=True)
    location = models.CharField(max_length=60, blank=False)
    slug = models.SlugField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.name)
        #this line below save every fields of the model instance
        super(Branch, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


    class Meta:
        ordering = [Lower('name')]
        
        
    def branch_operations(self):
        return self.branches.all()


        
        
class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, blank=False, unique=True)
    location = models.CharField(max_length=60, blank=False)
    slug = models.SlugField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.name)
        #this line below save every fields of the model instance
        super(Warehouse, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


    class Meta:
        ordering = [Lower('name')]

    def warehouse_operations(self):
        return self.warehouses.all()
      
        
        
class ServiceShop(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, blank=False, unique=True)
    location = models.CharField(max_length=60, blank=False)
    slug = models.SlugField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.name)
        #this line below save every fields of the model instance
        super(ServiceShop, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


    class Meta:
        ordering = [Lower('name')]

    def service_shop_operations(self):
        return self.service_shop.all()
