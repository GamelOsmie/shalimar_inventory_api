from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.functions import Lower
import uuid
from staff.models import Staff
from users.models import User

from vehicles.models import SparePart, Vehicle

# Create your models here.
class Branch(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
   
    name = models.CharField(max_length=60, blank=False, unique=True)
    location = models.CharField(max_length=60, blank=False)
    phone_number = models.CharField(max_length=13, blank=True)
   
     
    vehicles_in_stock = models.ManyToManyField(Vehicle, related_name ='branch_vehicles_in_stock', blank=True )
    vehicles_damaged = models.ManyToManyField(Vehicle, related_name ='branch_vehicles_damaged', blank=True )    
    vehicles_missing = models.ManyToManyField(Vehicle, related_name ='branch_vehicles_missing', blank=True )
    
    
    spare_parts_in_stock = models.ManyToManyField(SparePart, related_name ='branch_spare_parts_in_stock', blank=True )
    spare_parts_damaged = models.ManyToManyField(SparePart, related_name ='branch_spare_parts_damaged', blank=True )    
    spare_parts_missing = models.ManyToManyField(SparePart, related_name ='branch_spare_parts_missing', blank=True )
       
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.name)
        #this line below save every fields of the model instance
        super(Branch, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


    class Meta:
        ordering = [Lower('name')]
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        
    def vehicles_in_stock_count(self):
        return self.vehicles_in_stock.count()

    def vehicles_damaged_count(self):
        return self.vehicles_damaged.count()

    def vehicles_missing_count(self):
        return self.vehicles_missing.count()

    def spare_part_in_stock_count(self):
        return self.spare_parts_in_stock.count()

    def spare_part_damaged_count(self):
        return self.spare_parts_damaged.count()

    def spare_part_missing_count(self):
        return self.spare_parts_missing.count()
    
    def staff_count(self):
        return Staff.objects.filter(workplace=self.name).count()
    
        
    def users_count(self):
        return User.objects.filter(workplace=self.name).count()
           


        
        
class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    
    name = models.CharField(max_length=60, blank=False, unique=True)
    location = models.CharField(max_length=60, blank=False)
    phone_number = models.CharField(max_length=13, blank=True)
    
    vehicles_in_stock = models.ManyToManyField(Vehicle, related_name ='warehouse_vehicles_in_stock', blank=True )
    vehicles_damaged = models.ManyToManyField(Vehicle, related_name ='warehouse_vehicles_damaged', blank=True )    
    vehicles_missing = models.ManyToManyField(Vehicle, related_name ='warehouse_vehicles_missing', blank=True )
    
    spare_parts_in_stock = models.ManyToManyField(SparePart, related_name ='warehouse_spare_parts_in_stock', blank=True )
    spare_parts_damaged = models.ManyToManyField(SparePart, related_name ='warehouse_spare_parts_damaged', blank=True )    
    spare_parts_missing = models.ManyToManyField(SparePart, related_name ='warehouse_spare_parts_missing', blank=True )
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.name)
        #this line below save every fields of the model instance
        super(Warehouse, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


    class Meta:
        ordering = [Lower('name')]

    
    def vehicles_in_stock_count(self):
        return self.vehicles_in_stock.count()


    def vehicles_damaged_count(self):
        return self.vehicles_damaged.count()


    def vehicles_missing_count(self):
        return self.vehicles_missing.count()


    def spare_part_in_stock_count(self):
        return self.spare_parts_in_stock.count()


    def spare_part_damaged_count(self):
        return self.spare_parts_damaged.count()


    def spare_part_missing_count(self):
        return self.spare_parts_missing.count()
    
    def staff_count(self):
        return Staff.objects.filter(workplace=self.name).count()
    
        
    def users_count(self):
        return User.objects.filter(workplace=self.name).count()
      
      
        
        
class ServiceShop(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    
    name = models.CharField(max_length=60, blank=False, unique=True)
    location = models.CharField(max_length=60, blank=False)
    phone_number = models.CharField(max_length=13, blank=True)
    
    vehicles_in_stock = models.ManyToManyField(Vehicle, related_name ='service_shop_vehicles_in_stock', blank=True )
    vehicles_damaged = models.ManyToManyField(Vehicle, related_name ='service_shop_vehicles_damaged', blank=True )    
    vehicles_missing = models.ManyToManyField(Vehicle, related_name ='service_shop_vehicles_missing', blank=True )
    
    spare_parts_in_stock = models.ManyToManyField(SparePart, related_name ='service_shop_spare_parts_in_stock', blank=True )
    spare_parts_damaged = models.ManyToManyField(SparePart, related_name ='service_shop_spare_parts_damaged', blank=True )    
    spare_parts_missing = models.ManyToManyField(SparePart, related_name ='service_shop_spare_parts_missing', blank=True )
    
   
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.name)
        #this line below save every fields of the model instance
        super(ServiceShop, self).save(*args, **kwargs)

   
    def __str__(self):
        return self.name


    class Meta:
        ordering = [Lower('name')]

    def vehicles_in_stock_count(self):
        return self.vehicles_in_stock.count()


    def vehicles_damaged_count(self):
        return self.vehicles_damaged.count()


    def vehicles_missing_count(self):
        return self.vehicles_missing.count()


    def spare_part_in_stock_count(self):
        return self.spare_parts_in_stock.count()


    def spare_part_damaged_count(self):
        return self.spare_parts_damaged.count()


    def spare_part_missing_count(self):
        return self.spare_parts_missing.count()
    
    def staff_count(self):
        return Staff.objects.filter(workplace=self.name).count()
      
    
    def users_count(self):
        return User.objects.filter(workplace=self.name).count()
      
