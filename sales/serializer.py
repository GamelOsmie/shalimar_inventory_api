from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from units.serializers import BranchSerializer, WarehouseSerializer
from vehicles.serializers import SparePartSerializer, VehicleSerializer
from .models import *



class CustomerSerializer(ModelSerializer):
    fullname = serializers.ReadOnlyField()
    vehicles_purchased = serializers.ReadOnlyField()
    spare_parts_purchased = serializers.ReadOnlyField()
        
    class Meta:
        model = Customer
        fields = "__all__"



class OrganizationSerializer(ModelSerializer):
    vehicles_purchased = serializers.ReadOnlyField()
    spare_parts_purchased = serializers.ReadOnlyField()
    
    class Meta:
        model = Organization
        fields = "__all__"
        
    


class RetailSerializer(ModelSerializer):
    vehicle_qty = serializers.ReadOnlyField()
    spare_part_qty = serializers.ReadOnlyField()
    
    class Meta:
        model = Retail
        fields = "__all__"
        
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer).data
        response['branch'] = BranchSerializer(instance.branch).data['name']
        response['branch_location'] = BranchSerializer(instance.branch).data['location']
        response['phone_number'] = BranchSerializer(instance.branch).data['phone_number']
        response['spare_parts_sold'] = SparePartSerializer(instance.spare_parts_sold, many=True).data
        response['vehicles_sold'] = VehicleSerializer(instance.vehicles_sold, many=True).data
        return response




class WholesaleSerializer(ModelSerializer):
    vehicle_qty = serializers.ReadOnlyField()
    spare_part_qty = serializers.ReadOnlyField()
    
    class Meta:
        model = Wholesale
        fields = "__all__"

            
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['customer'] = CustomerSerializer(instance.customer).data
        response['warehouse'] = WarehouseSerializer(instance.warehouse).data['name']
        response['warehouse_location'] = WarehouseSerializer(instance.warehouse).data['location']
        response['phone_number'] = WarehouseSerializer(instance.warehouse).data['phone_number']
        response['spare_parts_sold'] = SparePartSerializer(instance.spare_parts_sold, many=True).data
        response['vehicles_sold'] = VehicleSerializer(instance.vehicles_sold, many=True).data
        return response



class FinanceAndCorporateSaleSerializer(ModelSerializer):
    vehicle_qty = serializers.ReadOnlyField()
    spare_part_qty = serializers.ReadOnlyField()
    
    
    class Meta:
        model = FinanceAndCorporateSale
        fields = "__all__"
        
        
                  
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['organization'] = CustomerSerializer(instance.organization).data
        response['supplier'] = WarehouseSerializer(instance.supplier).data['name']
        response['supplier_location'] = WarehouseSerializer(instance.supplier).data['location']
        response['phone_number'] = WarehouseSerializer(instance.supplier).data['phone_number']
        response['spare_parts_sold'] = SparePartSerializer(instance.spare_parts_sold, many=True).data
        response['vehicles_sold'] = VehicleSerializer(instance.vehicles_sold, many=True).data
        return response


