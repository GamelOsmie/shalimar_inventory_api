from pyexpat import model
from django.template.defaultfilters import slugify
from django.db.models.functions import Lower
from django.db import models
import uuid

# Create your models here.
class Tax(models.Model):
    rate = models.CharField(max_length=3, default=0)
    
    def save(self, *args, **kwargs):
        self.id = 1
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.rate


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    name = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = [Lower('name')]
        
    
    


class Model(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="brands")
    name = models.CharField(max_length=50, unique=True)
    
    purchase_price = models.CharField( max_length=10, blank=True, default=0)
    retail_price = models.CharField( max_length=10, blank=True, default=0)
    wholesale_price = models.CharField( max_length=10, blank=True, default=0)
    finance_sale_price = models.CharField( max_length=10, blank=True, default=0)
    corporate_sale_price = models.CharField( max_length=10, blank=True, default=0)
    
    # tax = models.ForeignKey(Tax, on_delete=models.PROTECT)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Model, self).save(*args, **kwargs)
    

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = [Lower('brand__name')]




class Vehicle(models.Model):
    location = (
        ('at sea', 'At Sea'),
        ('warehouse', 'Warehouse'),
        ('branch', 'Branch'),
        ('service station', 'Service Station'),
        ('finance sale', 'Finance Sale'),
        ('corporate sale', 'Corporate Sale'),
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail'),
        ('missing', 'Missing'),
    )
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    
    model = models.ForeignKey(Model, on_delete=models.PROTECT, blank=False, related_name="models")
    
    chassis_number = models.CharField(max_length=50, unique=True)
    engine_number = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=30, blank=True)
    
    current_location = models.CharField(max_length=20, choices=location, default="at sea")
    custodian =  models.CharField(max_length=100, blank=True)
    
    last_moved = models.DateTimeField(auto_now=True)
    
    purchase_price = models.CharField( max_length=10, blank=True, default=0)
    retail_price = models.CharField( max_length=10, blank=True, default=0)
    wholesale_price = models.CharField( max_length=10, blank=True, default=0)
    finance_sale_price = models.CharField( max_length=10, blank=True, default=0)
    corporate_sale_price = models.CharField( max_length=10, blank=True, default=0)
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.chassis_number)
        super(Vehicle, self).save(*args, **kwargs)

    def __str__(self):
        return self.chassis_number

    class Meta:
        ordering = [Lower('model__brand')]




class SparePartType(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)


    model = models.ForeignKey(Model, on_delete=models.PROTECT, blank=False, related_name="sparepart_models")         
    part = models.CharField(max_length=100, blank=False)
  
    purchase_price = models.CharField( max_length=10, blank=True, default=0)
    retail_price = models.CharField( max_length=10, blank=True, default=0)
    wholesale_price = models.CharField( max_length=10, blank=True, default=0)
    finance_sale_price = models.CharField( max_length=10, blank=True, default=0)
    corporate_sale_price = models.CharField( max_length=10, blank=True, default=0)
    
    # tax = models.ForeignKey(Tax, on_delete=models.PROTECT)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.part)
        super(SparePartType, self).save(*args, **kwargs)

    def __str__(self):
        return self.part

    class Meta:
        ordering = [Lower('model__brand')]



class SparePart(models.Model):
    location = (
        ('at sea', 'At Sea'),
        ('warehouse', 'Warehouse'),
        ('branch', 'Branch'),
        ('finance sale', 'Finance Sale'),
        ('corporate sale', 'Corporate Sale'),
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail')
    )
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    
    part_number = models.CharField(max_length=30, unique=True)
    part_type = models.ForeignKey(SparePartType, on_delete=models.PROTECT, blank=False, related_name="sparepart_type")         
    
    current_location = models.CharField(max_length=20, choices=location, default=None)
    custodian = models.CharField(max_length=100, blank=True, null=True)

    last_moved = models.DateTimeField(auto_now=True)
    
    purchase_price = models.CharField( max_length=10, blank=True, default=0)
    retail_price = models.CharField( max_length=10, blank=True, default=0)
    wholesale_price = models.CharField( max_length=10, blank=True, default=0)
    finance_sale_price = models.CharField( max_length=10, blank=True, default=0)
    corporate_sale_price = models.CharField( max_length=10, blank=True, default=0)
   
    def save(self, *args, **kwargs):
        self.slug = slugify(self.part)
        super(SparePart, self).save(*args, **kwargs)

    def __str__(self):
        return self.part_number

    class Meta:
        ordering = [Lower('part_number')]
