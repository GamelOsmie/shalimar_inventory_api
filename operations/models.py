from operator import contains
from os import link
from django.db import models
from django.template.defaultfilters import slugify
from units.models import Branch, ServiceShop, Warehouse
from vehicles.models import Vehicle, SparePart
from django.db.models.functions import Lower
import uuid
from shortuuid.django_fields import ShortUUIDField


class ProformaInvoice(models.Model):
   
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=30)
    invoice_date = models.DateField()
    document = models.FileField(upload_to='invoices/proforma')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number
    

    class Meta:
        ordering = ["-uploaded_at"]
        
    def associated_commercial_invoice(self):
        return self.commercial_invoices.all()
        

class CommercialInvoice(models.Model):
   
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=30)
    invoice_date = models.DateField()
    linked_proforma_invoice = models.OneToOneField(ProformaInvoice, on_delete=models.PROTECT, related_name="commercial_invoices", blank=False)
    document = models.FileField(upload_to='invoices/proforma')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number
    

    class Meta:
        ordering = ["-uploaded_at"]
        
        
        
class Shipment(models.Model):
    def default_journey_state(): 
       return {
        "status": "No", 
        "date": "",
        "comment": ""
    }
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    batch_number = models.CharField(max_length=20, blank=False, null=False)
    
    eta = models.DateField(blank=False, null=False)
    port_of_origin = models.CharField(max_length=250, blank=False, null=False)
    port_of_destination = models.CharField(max_length=250, blank=False, null=False)
    clearing_agent = models.CharField(max_length=50, blank=False, null=False)
      
    bill_of_lading_number = models.CharField(max_length=50, unique="true", blank=False, null=False)
    commercial_invoice = models.ForeignKey(CommercialInvoice, on_delete=models.PROTECT, related_name="commercial_invoices", blank=True, null=True )
    proforma_invoice = models.ForeignKey(ProformaInvoice, on_delete=models.PROTECT, related_name="proforma_invoices", blank=True, null=True )
        
    departs_embarkation_port = models.JSONField(default=default_journey_state)
    container_docks_at_disembarkation_port = models.JSONField(default=default_journey_state)
    declaration_of_invoice_for_payment = models.JSONField(default=default_journey_state)
    make_ctn_payment = models.JSONField(default=default_journey_state)
    intertek_payment = models.JSONField(default=default_journey_state)
    delivery_order_payment = models.JSONField(default=default_journey_state)
    port_charges_payment = models.JSONField(default=default_journey_state)
    container_scan = models.JSONField(default=default_journey_state)
    asycuda_system_input = models.JSONField(default=default_journey_state)
    examination_of_goods = models.JSONField(default=default_journey_state)
    release_order_given_at_the_port = models.JSONField(default=default_journey_state)
    container_exist_port = models.JSONField(default=default_journey_state)
    container_arrives_at_warehouse = models.JSONField(default=default_journey_state)
    container_offloaded = models.JSONField(default=default_journey_state)
    container_to_shipping = models.JSONField(default=default_journey_state)
    confirmation_of_vehicle_quantity = models.JSONField(default=default_journey_state)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.batch_number)
        #this line below save every fields of the model instance
        super(Shipment, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.batch_number
    
    
    class Meta:
        ordering = ["-created_at"]
    
    
    def containers(self):
        return self.contains.all()
    
    
    def container_count(self):
        return self.contains.all().count()
    
    
    
class Container(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    container_number = models.CharField(max_length=20, blank=False)
    
    content_type = models.CharField(max_length=20, blank=True)
    
    vehicles = models.ManyToManyField(Vehicle, related_name ='container_vehicles', blank=True)

    spare_parts = models.ManyToManyField(SparePart, related_name ='container_spare_parts', blank=True)
    
    shipment_batch = models.ForeignKey(Shipment, on_delete=models.PROTECT, blank=True, null=True,related_name="contains")
    

    def save(self, *args, **kwargs):        
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.container_number)
        #this line below save every fields of the model instance
        super(Container, self).save(*args, **kwargs)


    def __str__(self):
        return self.container_number
    
    
    def vehicle_count(self):
        return self.vehicles.count()
    
    
    def spare_parts_count(self):
        return self.spare_parts.count()


    
class BranchOperation(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    
    branch = models.OneToOneField(Branch, on_delete=models.PROTECT, related_name="branches")
    
    vehicles_in_stock = models.ManyToManyField(Vehicle, related_name ='branch_vehicles_in_stock', blank=True )
    vehicles_damaged = models.ManyToManyField(Vehicle, related_name ='branch_vehicles_damaged', blank=True )    
    vehicles_damaged = models.ManyToManyField(Vehicle, related_name ='branch_vehicles_missing', blank=True )
    
    
    spare_parts_in_stock = models.ManyToManyField(SparePart, related_name ='branch_spare_parts_in_stock', blank=True )
    spare_parts_damaged = models.ManyToManyField(SparePart, related_name ='branch_spare_parts_damaged', blank=True )    
    spare_parts_damaged = models.ManyToManyField(SparePart, related_name ='branch_spare_parts_missing', blank=True )
    
    class Meta:
        ordering = [Lower('branch__name')]
        
        

    def vehicles_in_stock_count(self):
        return self.vehicles_in_stock.count()


    def vehicles_damaged_count(self):
        return self.vehicles_damaged.count()


    def vehicles_missing_count(self):
        return self.vehicles_missing.count()


    def spare_part_in_stock_count(self):
        return self.spare_part_in_stock.count()


    def spare_part_damaged_count(self):
        return self.spare_part_damaged.count()


    def spare_part_missing_count(self):
        return self.spare_part_missing.count()
   

     
        
class WarehouseOperation(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    
    warehouse = models.OneToOneField(Warehouse, on_delete=models.PROTECT, related_name="warehouses")
    
    vehicles_in_stock = models.ManyToManyField(Vehicle, related_name ='warehouse_vehicles_in_stock', blank=True )
    vehicles_damaged = models.ManyToManyField(Vehicle, related_name ='warehouse_vehicles_damaged', blank=True )    
    vehicles_missing = models.ManyToManyField(Vehicle, related_name ='warehouse_vehicles_missing', blank=True )
    
    spare_parts_in_stock = models.ManyToManyField(SparePart, related_name ='warehouse_spare_parts_in_stock', blank=True )
    spare_parts_damaged = models.ManyToManyField(SparePart, related_name ='warehouse_spare_parts_damaged', blank=True )    
    spare_parts_missing = models.ManyToManyField(SparePart, related_name ='warehouse_spare_parts_missing', blank=True )
     

    class Meta:
        ordering = [Lower('warehouse__name')]
     

    def vehicles_in_stock_count(self):
        return self.vehicles_in_stock.count()


    def vehicles_damaged_count(self):
        return self.vehicles_damaged.count()


    def vehicles_missing_count(self):
        return self.vehicles_missing.count()


    def spare_part_in_stock_count(self):
        return self.spare_part_in_stock.count()


    def spare_part_damaged_count(self):
        return self.spare_part_damaged.count()


    def spare_part_missing_count(self):
        return self.spare_part_missing.count()
    
    
     
class ServiceShopOperation(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    
    service_shop = models.OneToOneField(ServiceShop, on_delete=models.PROTECT, related_name="service_shops")
    
    vehicles_in_stock = models.ManyToManyField(Vehicle, related_name ='service_shop_vehicles_in_stock', blank=True )
    vehicles_damaged = models.ManyToManyField(Vehicle, related_name ='service_shop_vehicles_damaged', blank=True )    
    vehicles_missing = models.ManyToManyField(Vehicle, related_name ='service_shop_vehicles_missing', blank=True )
    
    spare_parts_in_stock = models.ManyToManyField(SparePart, related_name ='service_shop_spare_parts_in_stock', blank=True )
    spare_parts_damaged = models.ManyToManyField(SparePart, related_name ='service_shop_spare_parts_damaged', blank=True )    
    spare_parts_missing = models.ManyToManyField(SparePart, related_name ='service_shop_spare_parts_missing', blank=True )
     

    class Meta:
        ordering = [Lower('warehouse__name')]
     

    def vehicles_in_stock_count(self):
        return self.vehicles_in_stock.count()


    def vehicles_damaged_count(self):
        return self.vehicles_damaged.count()


    def vehicles_missing_count(self):
        return self.vehicles_missing.count()


    def spare_part_in_stock_count(self):
        return self.spare_part_in_stock.count()


    def spare_part_damaged_count(self):
        return self.spare_part_damaged.count()


    def spare_part_missing_count(self):
        return self.spare_part_missing.count()
    
    
    
class WareSupply(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    supply_code = ShortUUIDField(length=8, max_length=10, prefix="WS", alphabet="1234567890", editable=False)
    
    container = models.ForeignKey(Container, on_delete=models.PROTECT, blank=False, related_name="warehouse_supply")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, blank=False, related_name="warehouse_supply")
    
    vehicles_supplied = models.ManyToManyField(Vehicle, related_name ='warehouse_vehicles_supplied', blank=True)
    vehicles_supplied_quantity = models.CharField(max_length=10, blank=True)
    vehicles_supplied_received = models.CharField(max_length=10, blank=True, default=0)

    spare_parts_supplied = models.ManyToManyField(SparePart, related_name ='warehouse_spare_parts_supplied', blank=True)
    spare_parts_supplied_quantity = models.CharField(max_length=10, blank=True)
    spare_parts_supplied_received = models.CharField(max_length=10, blank=True, default=0)

    supply_date = models.DateTimeField(auto_now_add=True)
    received_date = models.DateTimeField(blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.supply_code)
        super(WareSupply, self).save(*args, **kwargs)

    def __str__(self):
        return self.container_number



    