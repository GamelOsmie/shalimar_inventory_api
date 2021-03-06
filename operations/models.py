
from django.db import models
from django.template.defaultfilters import slugify
from units.models import Branch, ServiceShop, Warehouse
from vehicles.models import Vehicle, SparePart
from django.db.models.functions import Lower
import uuid
from shortuuid.django_fields import ShortUUIDField


class ProformaInvoice(models.Model):
   
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=30, unique=True)
    invoice_date = models.DateField()
    document = models.FileField(upload_to='invoices/proforma')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number
    

    class Meta:
        ordering = ["-uploaded_at"]
        

        

class CommercialInvoice(models.Model):
   
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=30, unique=True)
    invoice_date = models.DateField()
    linked_proforma_invoice = models.OneToOneField(ProformaInvoice, on_delete=models.PROTECT, related_name="commercial_invoices", blank=False)
    document = models.FileField(upload_to='invoices/commercial')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number
    

    class Meta:
        ordering = ["-uploaded_at"]
        
        
        
class Shipment(models.Model):
    def default_journey_state(): 
       return {
        "status": "no", 
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
    commercial_invoice = models.ForeignKey(CommercialInvoice, on_delete=models.PROTECT, related_name="shipments_commercial_invoices", blank=True, null=True )
    proforma_invoice = models.ForeignKey(ProformaInvoice, on_delete=models.PROTECT, related_name="shipments_proforma_invoices", blank=True, null=True )
        
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
    
    on_the_move = models.BooleanField(default=False)
    departed_at = models.DateTimeField(blank=True, null=True)
    
    
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
    slug = slug = models.SlugField(max_length=50, blank=True)
    container_number = models.CharField(max_length=20, blank=False, unique=True)
    
    content_type = models.CharField(max_length=20, blank=True)
    
    vehicles = models.ManyToManyField(Vehicle, related_name ='container_vehicles', blank=True)

    spare_parts = models.ManyToManyField(SparePart, related_name ='container_spare_parts', blank=True)
    
    shipment_batch = models.ForeignKey(Shipment, on_delete=models.PROTECT, blank=True, null=True, related_name="contains")
    

    def save(self, *args, **kwargs):        
        #this line below give to the instance slug field a slug name
        self.slug = slugify(self.container_number)
        #this line below save every fields of the model instance
        super(Container, self).save(*args, **kwargs)


    def __str__(self):
        return self.container_number
    
    
    def vehicle_count(self):
        return self.vehicles.count()
    
    
    def spare_part_count(self):
        return self.spare_parts.count()
    
    
    def spare_part_supplies(self):
        return self.container_spare_parts.all()
    
    
    def vehicle_supplies(self):
        return self.container_vehicles.all()



    
class WarehouseVehiclesSupply(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    supply_code = ShortUUIDField(length=7, max_length=10, prefix="WVS", alphabet="1234567890", editable=False, unique=True)
    
    container = models.ForeignKey(Container, on_delete=models.PROTECT, blank=False, related_name="container_vehicles")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, blank=False, related_name="vehicle_warehouses")
    
    vehicles_supplied = models.ManyToManyField(Vehicle, related_name ='warehouse_vehicles_supplied', blank=True)
    vehicles_supplied_quantity = models.CharField(max_length=10, blank=True)
    vehicles_supplied_received = models.CharField(max_length=10, blank=True, default=0)

    supply_date = models.DateTimeField(auto_now_add=True)
    received_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.supply_code)
        super(WarehouseVehiclesSupply, self).save(*args, **kwargs)

    def __str__(self):
        return self.supply_code
    
    class Meta:
        ordering = ['-supply_date']

    
class WarehouseSparePartsSupply(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    supply_code = ShortUUIDField(length=7, max_length=10, prefix="WPS", alphabet="1234567890", editable=False, unique=True)
    
    container = models.ForeignKey(Container, on_delete=models.PROTECT, blank=False, related_name="container_spare_parts")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, blank=False, related_name="spare_part_warehouses")
    
    spare_parts_supplied = models.ManyToManyField(SparePart, related_name ='warehouse_spare_parts_supplied', blank=True)
    spare_parts_supplied_quantity = models.CharField(max_length=10, blank=True)
    spare_parts_supplied_received = models.CharField(max_length=10, blank=True, default=0)

    supply_date = models.DateTimeField(auto_now_add=True)
    received_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.supply_code)
        super(WarehouseSparePartsSupply, self).save(*args, **kwargs)

    def __str__(self):
        return self.supply_code
    
    
    class Meta:
        ordering = ['-supply_date']



    
class BranchVehiclesSupply(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    supply_code = ShortUUIDField(length=7, max_length=10, prefix="BVS", alphabet="1234567890", editable=False, unique=True)
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, blank=False, related_name="warehouse_vehicles_for_supply")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, blank=False, related_name="vehicle_branches")
    
    vehicles_supplied = models.ManyToManyField(Vehicle, related_name ='branch_vehicles_supplied', blank=True)
    vehicles_supplied_quantity = models.CharField(max_length=10, blank=True)
    vehicles_supplied_received = models.CharField(max_length=10, blank=True, default=0)

    supply_date = models.DateTimeField(auto_now_add=True)
    received_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.supply_code)
        super(BranchVehiclesSupply, self).save(*args, **kwargs)

    def __str__(self):
        return self.supply_code
    
    class Meta:
        ordering = ['-supply_date']
    
   

    
class BranchSparePartsSupply(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=50, blank=True)
    supply_code = ShortUUIDField(length=7, max_length=10, prefix="BPS", alphabet="1234567890", editable=False, unique=True)
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, blank=False, related_name="warehouse_spare_part_for_supply")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, blank=False, related_name="spare_part_branches")
    
    spare_parts_supplied = models.ManyToManyField(SparePart, related_name ='branch_vehicles_supplied', blank=True)
    spare_parts_supplied_quantity = models.CharField(max_length=10, blank=True)
    spare_parts_supplied_received = models.CharField(max_length=10, blank=True, default=0)

    supply_date = models.DateTimeField(auto_now_add=True)
    received_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.supply_code)
        super(BranchSparePartsSupply, self).save(*args, **kwargs)

    def __str__(self):
        return self.supply_code
    
    
    class Meta:
        ordering = ['-supply_date']
        
        
        

    

    