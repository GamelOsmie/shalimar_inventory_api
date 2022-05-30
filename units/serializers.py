from threading import local
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

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


    class Meta:
        model = Branch
        fields = "__all__"
        
        def to_representation(self, instance):
            response = super().to_representation(instance)
            response["vehicles"] = VehicleSerializer(instance.vehicles.all(), many=True).data
            response["spare_parts"] = SparePartSerializer(instance.spare_parts.all(), many=True).data
            return response
        

class WarehouseDetailSerializer(ModelSerializer):
    vehicles_in_stock_count = serializers.ReadOnlyField()
    vehicles_damaged_count = serializers.ReadOnlyField()
    vehicles_missing_count = serializers.ReadOnlyField()

    spare_part_in_stock_count = serializers.ReadOnlyField()
    spare_part_damaged_count = serializers.ReadOnlyField()
    spare_part_missing_count = serializers.ReadOnlyField()
    
    staff_count = serializers.ReadOnlyField()
    users_count = serializers.ReadOnlyField()


    class Meta:
        model = Warehouse
        fields = "__all__"
        
        def to_representation(self, instance):
            response = super().to_representation(instance)
            response["vehicles"] = VehicleSerializer(instance.vehicles.all(), many=True).data
            response["spare_parts"] = SparePartSerializer(instance.spare_parts.all(), many=True).data
            return response
        
        

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
        
        def to_representation(self, instance):
            response = super().to_representation(instance)
            response["vehicles"] = VehicleSerializer(instance.vehicles.all(), many=True).data
            response["spare_parts"] = SparePartSerializer(instance.spare_parts.all(), many=True).data
            return response
        
