from pyexpat import model
from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from django.db.models.functions import Lower
from django.template.defaultfilters import slugify
from units.models import Branch, Warehouse

from vehicles.models import Vehicle



class Customer(models.Model):
    customer_types = (
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('finance sale', 'Finance Sale'),
        ('corporate sale', 'Corporate Sale'),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    
    first_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=False)
    
    phone_number = models.CharField(max_length=15, blank=False)
    email = models.CharField(max_length=200, blank=True)
    
    customer_type = models.CharField(max_length=50, blank=True, null=True, choices=customer_types)
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
 
    class Meta:
        ordering = [Lower("first_name"), Lower("last_name")]

    
class Retail(models.Model):
          
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    invoice_number = ShortUUIDField(length=7, max_length=10, prefix="STL", alphabet="1234567890", editable=False, unique=True)
    
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    vehicles_sold = models.ManyToManyField(Vehicle, related_name ='retail_vehicle_sales', blank=True)
    spare_parts_sold = models.ManyToManyField(Vehicle, related_name ='retail_spare_part_sales', blank=True)
    
    sold_at = models.DateTimeField(auto_now_add=True)
    
     
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.invoice_number)
        #this line below save every fields of the model instance
        super(Retail, self).save(*args, **kwargs)


    def __str__(self):
        return self.invoice_number
    

    class Meta:
        ordering = ["-sold_at"]
        
        
    
class Wholesale(models.Model):
          
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    invoice_number = ShortUUIDField(length=7, max_length=10, prefix="STL", alphabet="1234567890", editable=False, unique=True)
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    vehicles_sold = models.ManyToManyField(Vehicle, related_name ='wholesale_vehicle_sales', blank=True)
    spare_parts_sold = models.ManyToManyField(Vehicle, related_name ='wholesale_spare_part_sales', blank=True)
    
    sold_at = models.DateTimeField(auto_now_add=True)
    
        
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.invoice_number)
        #this line below save every fields of the model instance
        super(Wholesale, self).save(*args, **kwargs)


    def __str__(self):
        return self.invoice_number
    

    class Meta:
        ordering = ["-sold_at"]
        
   
    
class FinanceAndCorporateSale(models.Model):
    
    sale_types = (
        ('finance sale', 'Finance Sale'),
        ('corporate sale', 'Corporate Sale'),
    )
          
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    invoice_number = ShortUUIDField(length=7, max_length=10, prefix="STL", alphabet="1234567890", editable=False, unique=True)
    
    customer_type = models.CharField(max_length=50, blank=True, null=True, choices=sale_types)
    
    supplier = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    vehicles_sold = models.ManyToManyField(Vehicle, related_name ='finance_and_corporate_vehicle_sales', blank=True)
    spare_parts_sold = models.ManyToManyField(Vehicle, related_name ='finance_and_corporate_spare_part_sales', blank=True)
    
    sold_at = models.DateTimeField(auto_now_add=True)
    
        
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.invoice_number)
        #this line below save every fields of the model instance
        super(FinanceAndCorporateSale, self).save(*args, **kwargs)


    def __str__(self):
        return self.invoice_number
    

    class Meta:
        ordering = ["-sold_at"]