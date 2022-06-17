from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from operations.serializers import BranchSparePartsSupplySerializer, BranchVehiclesSupplySerializer

from vehicles.serializers import SparePartSerializer, VehicleSerializer

from .models import *


class BranchSerializer(ModelSerializer):

    class Meta:
        model = Branch
        fields = ('slug', 'id', 'name', 'location', 'phone_number')
        

class WarehouseSerializer(ModelSerializer):

    class Meta:
        model = Warehouse
        fields = ('slug', 'id', 'name', 'location', 'phone_number')
        

class ServiceShopSerializer(ModelSerializer):

    class Meta:
        model = ServiceShop
        fields = ('slug', 'id', 'name', 'location', 'phone_number')
        

class BranchDetailSerializer(ModelSerializer):
    vehicles_in_stock_count = serializers.ReadOnlyField()
    vehicles_damaged_count = serializers.ReadOnlyField()
    vehicles_missing_count = serializers.ReadOnlyField()

    spare_part_in_stock_count = serializers.ReadOnlyField()
    spare_part_damaged_count = serializers.ReadOnlyField()
    spare_part_missing_count = serializers.ReadOnlyField()
    
    staff_count = serializers.ReadOnlyField()
    users_count = serializers.ReadOnlyField()
    expected_vehicles = serializers.ReadOnlyField()
    expected_spare_parts = serializers.ReadOnlyField()
    

    class Meta:
        model = Branch
        fields = "__all__"
        depth = 3

   

class WarehouseDetailSerializer(ModelSerializer):
    vehicles_in_stock_count = serializers.ReadOnlyField()
    vehicles_damaged_count = serializers.ReadOnlyField()
    vehicles_missing_count = serializers.ReadOnlyField()

    spare_part_in_stock_count = serializers.ReadOnlyField()
    spare_part_damaged_count = serializers.ReadOnlyField()
    spare_part_missing_count = serializers.ReadOnlyField()
    
    staff_count = serializers.ReadOnlyField()
    users_count = serializers.ReadOnlyField()
    expected_vehicles = serializers.ReadOnlyField()
    expected_spare_parts = serializers.ReadOnlyField()
    
    vehicle_supply = BranchVehiclesSupplySerializer(source='warehouse_vehicles_for_supply', many=True, read_only=True)
    spare_part_supply = BranchSparePartsSupplySerializer(source='warehouse_spare_part_for_supply', many=True, read_only=True)


    class Meta:
        model = Warehouse
        fields = "__all__"
        depth = 3
    
        

class ServiceShopDetailSerializer(ModelSerializer):
    vehicles_in_stock_count = serializers.ReadOnlyField()
    vehicles_damaged_count = serializers.ReadOnlyField()
    vehicles_missing_count = serializers.ReadOnlyField()

    spare_part_in_stock_count = serializers.ReadOnlyField()
    spare_part_damaged_count = serializers.ReadOnlyField()
    spare_part_missing_count = serializers.ReadOnlyField()
    
    staff_count = serializers.ReadOnlyField()
    users_count = serializers.ReadOnlyField()


    class Meta:
        model = ServiceShop
        fields = "__all__"
        depth = 3
