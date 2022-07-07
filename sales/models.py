from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField
from django.db.models.functions import Lower
from django.template.defaultfilters import slugify
from units.models import Branch, Warehouse

from vehicles.models import SparePart, Vehicle


class Customer(models.Model):
    customer_types = (
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    
    first_name = models.CharField(max_length=50, blank=False)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=False)
    
    phone_number = models.CharField(max_length=15, blank=False)
    email = models.CharField(max_length=200, blank=True)
    
    customer_type = models.CharField(max_length=50, blank=True, null=True, choices=customer_types, default=None)
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
 
    class Meta:
        ordering = [Lower("first_name"), Lower("last_name")]
        
        
    def fullname(self):
        if self.first_name == None:
            first_name = ""
        else:
            first_name = self.first_name

        if self.middle_name == None:
            middle_name = ""
        else:
            middle_name = self.middle_name

        if self.last_name == None:
            last_name = ""
        else:
            last_name = self.last_name

        name = f"{first_name} {middle_name} {last_name}"

        return name


    def vehicles_purchased(self):
        
        if self.customer_type == "retail":
            purchases = self.retail_customers.all()
            vehicles_qty = 0
            
            for purchase in purchases:
                vehicles_qty += len(purchase.vehicles_sold.values())
            
            return vehicles_qty 
        
        
        if self.customer_type == "wholesale":
            purchases = self.wholesale_customers.all()
            vehicles_qty = 0

            for purchase in purchases:
                vehicles_qty += len(purchase.vehicles_sold.values())

            return vehicles_qty
        

    def spare_parts_purchased(self):
        
        if self.customer_type == "retail":
            purchases = self.retail_customers.all()
            vehicles_qty = 0
            
            for purchase in purchases:
                vehicles_qty += len(purchase.spare_parts_sold.values())
            
            return vehicles_qty 
        
        
        if self.customer_type == "wholesale":
            purchases = self.wholesale_customers.all()
            vehicles_qty = 0

            for purchase in purchases:
                vehicles_qty += len(purchase.spare_parts_sold.values())

            return vehicles_qty
        


class Organization(models.Model):
    consumption_types = (
        ('finance sale', 'Finance Sale'),
        ('corporate sale', 'Corporate Sale'),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=150, blank=False)
    
    address = models.CharField(max_length=150, blank=False)
    location = models.CharField(max_length=50, blank=False)

    phone_number = models.CharField(max_length=15, blank=False)
    email = models.CharField(max_length=200, blank=True)

    consumption_type = models.CharField(max_length=50, blank=True, null=True, choices=consumption_types, default=None)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = [Lower("name")]
        
        
        
    def vehicles_purchased(self):
        purchases = self.corporate_customers.all()
        vehicles_qty = 0

        for purchase in purchases:
            vehicles_qty += len(purchase.vehicles_sold.values())

        return vehicles_qty
        

    def spare_parts_purchased(self):
        purchases = self.corporate_customers.all()
        vehicles_qty = 0

        for purchase in purchases:
            vehicles_qty += len(purchase.spare_parts_sold.values())

        return vehicles_qty


    
class Retail(models.Model):
          
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    invoice_number = ShortUUIDField(length=7, max_length=10, prefix="STL", alphabet="1234567890", editable=False, unique=True)
    
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="branch_sales")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='retail_customers')
    
    vehicles_sold = models.ManyToManyField(Vehicle, related_name ='retail_vehicle_sales', blank=True)
    spare_parts_sold = models.ManyToManyField(SparePart, related_name ='retail_spare_part_sales', blank=True)
    
    discount = models.CharField(max_length=2, blank=True, null=True ,default=0)
    tax = models.CharField(max_length=2, blank=True, null=True, default=0)
    
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
        
    @property
    def vehicle_qty(self):
        return self.vehicles_sold.count()
    
    @property
    def spare_part_qty(self):
        return self.spare_parts_sold.count()
        
    
class Wholesale(models.Model):
          
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    invoice_number = ShortUUIDField(length=7, max_length=10, prefix="STL", alphabet="1234567890", editable=False, unique=True)
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="warehouse_sales")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='wholesale_customers')
    
    vehicles_sold = models.ManyToManyField(Vehicle, related_name ='wholesale_vehicle_sales', blank=True)
    spare_parts_sold = models.ManyToManyField(SparePart, related_name ='wholesale_spare_part_sales', blank=True)
    
    discount = models.CharField(max_length=2, blank=True, null=True, default=0)
    tax = models.CharField(max_length=2, blank=True, null=True, default=0)
    
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
        
        
    @property    
    def vehicle_qty(self):
        return self.vehicles_sold.count()
    @property
    def spare_part_qty(self):
        return self.spare_parts_sold.count()
    

    
class FinanceAndCorporateSale(models.Model):
    
    sale_types = (
        ('finance sale', 'Finance Sale'),
        ('corporate sale', 'Corporate Sale'),
    )
          
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    invoice_number = ShortUUIDField(length=7, max_length=10, prefix="STL", alphabet="1234567890", editable=False, unique=True)
    
    sale_type = models.CharField(max_length=50, blank=True, null=True, choices=sale_types)
    
    supplier = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, related_name='corporate_customers')
    
    vehicles_sold = models.ManyToManyField(Vehicle, related_name ='finance_and_corporate_vehicle_sales', blank=True)
    spare_parts_sold = models.ManyToManyField(SparePart, related_name ='finance_and_corporate_spare_part_sales', blank=True)
    
    discount = models.CharField(max_length=2, blank=True, null=True, default=0)
    tax = models.CharField(max_length=2, blank=True, null=True, default=0)
    
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
        
    @property
    def vehicle_qty(self):
        return self.vehicles_sold.count()

    @property
    def spare_part_qty(self):
        return self.spare_parts_sold.count()
