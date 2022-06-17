from rest_framework import serializers
from .models import  BranchSparePartsSupply, BranchVehiclesSupply, CommercialInvoice, ProformaInvoice, Shipment, Container, WarehouseSparePartsSupply, WarehouseVehiclesSupply
from vehicles.serializers import SparePartSerializer, VehicleSerializer



class CommercialInvoiceSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = CommercialInvoice
        fields = "__all__"
        
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["linked_proforma_invoice"] = ProformaInvoiceSerializer(instance.linked_proforma_invoice).data
        return response
        

class ProformaInvoiceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ProformaInvoice
        fields = "__all__"
 
 
class ShipmentListSerializer(serializers.ModelSerializer):
    container_count = serializers.ReadOnlyField()
 
    class Meta:
        model = Shipment
        fields = ["id", "slug", "batch_number", "port_of_origin", "port_of_destination", "eta", "container_count", "container_exist_port", "departed_at"]
        
        

class WarehouseVehiclesSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WarehouseVehiclesSupply
        fields = "__all__"
        
    
    def to_representation(self, instance):
        from units.serializers import WarehouseSerializer
        response = super().to_representation(instance)
        response["warehouse"] = WarehouseSerializer(instance.warehouse).data['name']
        response["container"] = ContainerSerializer(instance.container).data['container_number']
        response["vehicles_supplied"] = VehicleSerializer(instance.vehicles_supplied.all(), many=True).data
        return response
        
        

class BranchVehiclesSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BranchVehiclesSupply
        fields = "__all__"
        
    
    def to_representation(self, instance):
        from units.serializers import BranchSerializer, WarehouseSerializer
        response = super().to_representation(instance)
        response["warehouse"] = WarehouseSerializer(instance.warehouse).data['name']
        response["branch"] = BranchSerializer(instance.branch).data['name']
        response["vehicles_supplied"] = VehicleSerializer(instance.vehicles_supplied.all(), many=True).data
        return response
        
        

class BranchSparePartsSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BranchSparePartsSupply
        fields = "__all__"
        
    
    def to_representation(self, instance):
        from units.serializers import BranchSerializer, WarehouseSerializer
        response = super().to_representation(instance)
        response["warehouse"] = WarehouseSerializer(instance.warehouse).data['name']
        response["branch"] = BranchSerializer(instance.branch).data['name']
        response["spare_parts_supplied"] = SparePartSerializer(instance.spare_parts_supplied.all(), many=True).data
        return response
    


class WarehouseSparePartsSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WarehouseSparePartsSupply
        fields = "__all__"
        
    
    def to_representation(self, instance):
        from units.serializers import WarehouseSerializer
        response = super().to_representation(instance)
        response["warehouse"] = WarehouseSerializer(instance.warehouse).data['name']
        response["container"] = ContainerSerializer(instance.container).data['container_number']
        response["spare_parts_supplied"] = SparePartSerializer(instance.spare_parts_supplied.all(), many=True).data
        return response

    

class ContainerSerializer(serializers.ModelSerializer):
    vehicle_count = serializers.ReadOnlyField()
    spare_part_count = serializers.ReadOnlyField()

    class Meta:
        model = Container
        # fields = "__all__"
        exclude = ['vehicles', 'spare_parts']
    

class ContainerDetailSerializer(serializers.ModelSerializer):
    vehicle_count = serializers.ReadOnlyField()
    spare_part_count = serializers.ReadOnlyField()
    vehicle_supply = WarehouseVehiclesSupplySerializer(source='vehicle_supplies', many=True, read_only=True)
    spare_part_supply = WarehouseSparePartsSupplySerializer(source='spare_part_supplies', many=True, read_only=True)

    class Meta:
        model = Container
        fields = ("__all__")


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["vehicles"] = VehicleSerializer(instance.vehicles.all(), many=True).data
        response["spare_parts"] = SparePartSerializer(instance.spare_parts.all(), many=True).data
        response["shipment_batch"] = ShipmentListSerializer(instance.shipment_batch).data['batch_number']
        return response




class ShipmentDetailSerializer(serializers.ModelSerializer):
    shipment_containers = ContainerSerializer(source='containers', many=True, read_only=True)
    container_count = serializers.ReadOnlyField()

    class Meta:
        model = Shipment
        fields = ("__all__")
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["proforma_invoice"] = ProformaInvoiceSerializer(instance.proforma_invoice).data
        response["commercial_invoice"] = CommercialInvoiceSerializer(instance.commercial_invoice).data
        return response

