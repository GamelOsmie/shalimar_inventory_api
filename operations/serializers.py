from rest_framework import serializers

from units.serializers import BranchSerializer, WarehouseSerializer
from .models import  CommercialInvoice, ProformaInvoice, Shipment, Container, WareSupply
from vehicles.serializers import VehicleSerializer



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




class WarehouseSupplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WareSupply
        fields = "__all__"
        
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["warehouse"] = WarehouseSerializer(instance.warehouse.all(), many=True).data['warehouse']['name']
        response["container"] = ContainerSerializer(instance.container.all(), many=True).data['container_number']
        return response

