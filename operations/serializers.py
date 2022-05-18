from rest_framework import serializers

from units.serializers import BranchSerializer, WarehouseSerializer
from .models import BranchOperation, CommercialInvoice, ProformaInvoice, ServiceShopOperation, Shipment, Container, WareSupply, WarehouseOperation
from vehicles.serializers import VehicleSerializer



class CommercialInvoiceSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = CommercialInvoice
        fields = "__all__"
        
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["liked_proforma_invoice"] = ProformaInvoiceSerializer(instance.liked_proforma_invoice).data
        return response
        

class ProformaInvoiceSerializer(serializers.ModelSerializer):
    linked_commercial_invoice = CommercialInvoiceSerializer(source='associated_commercial_invoice', many=False, read_only=True)
    
    class Meta:
        model = ProformaInvoice
        fields = "__all__"
        
        


class ContainerSerializer(serializers.ModelSerializer):
    vehicle_count = serializers.ReadOnlyField()
    spare_part_count = serializers.ReadOnlyField()
    # vehicles_type = serializers.ReadOnlyField()

    class Meta:
        model = Container
        fields = "__all__"


    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["vehicles"] = VehicleSerializer(instance.vehicles.all(), many=True).data
        response["spare_parts"] = VehicleSerializer(instance.spare_parts.all(), many=True).data
        return response


class ShipmentListSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Shipment
        fields = ["id","slug","batch_number", "port_of_origin", "port_of_destination", "eta"]


class ShipmentDetailSerializer(serializers.ModelSerializer):
    shipment_containers = ContainerSerializer(source='containers', many=True, read_only=True)
    container_count = serializers.ReadOnlyField()

    class Meta:
        model = Shipment
        fields = ("__all__")



class BranchOperationSerializer(serializers.ModelSerializer):
    vehicles_in_stock_count = serializers.ReadOnlyField()
    vehicles_damaged_count = serializers.ReadOnlyField()
    vehicles_missing_count = serializers.ReadOnlyField()
    
    spare_part_in_stock_count = serializers.ReadOnlyField()
    spare_part_damaged_count = serializers.ReadOnlyField()
    spare_part_missing_count = serializers.ReadOnlyField()
    
    class Meta:
        model = BranchOperation
        fields = "__all__"
        
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["branch"] = BranchSerializer(instance.branch).data
        return response

    

class WarehouseOperationSerializer(serializers.ModelSerializer):
    vehicles_in_stock_count = serializers.ReadOnlyField()
    vehicles_damaged_count = serializers.ReadOnlyField()
    vehicles_missing_count = serializers.ReadOnlyField()
    
    spare_part_in_stock_count = serializers.ReadOnlyField()
    spare_part_damaged_count = serializers.ReadOnlyField()
    spare_part_missing_count = serializers.ReadOnlyField()
    
    class Meta:
        model = WarehouseOperation
        fields = "__all__"
        
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["warehouse"] = WarehouseSerializer(instance.warehouse).data
        return response


class ServiceShopOperationSerializer(serializers.ModelSerializer):
    vehicles_in_stock_count = serializers.ReadOnlyField()
    vehicles_damaged_count = serializers.ReadOnlyField()
    vehicles_missing_count = serializers.ReadOnlyField()
    
    spare_part_in_stock_count = serializers.ReadOnlyField()
    spare_part_damaged_count = serializers.ReadOnlyField()
    spare_part_missing_count = serializers.ReadOnlyField()
    
    class Meta:
        model = ServiceShopOperation
        fields = "__all__"
        
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["service_shop"] = ServiceShopOperationSerializer(instance.service_shop).data
        return response



class WarehouseSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WareSupply
        fields = "__all__"
        
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["warehouse"] = WarehouseOperationSerializer(instance.warehouse.all(), many=True).data['warehouse']['name']
        response["container"] = ContainerSerializer(instance.container.all(), many=True).data['container_number']
        return response

