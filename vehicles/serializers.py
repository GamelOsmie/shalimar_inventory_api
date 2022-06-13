from rest_framework.serializers import ModelSerializer
from .models import *



class TaxSerializer(ModelSerializer):
    
    class Meta:
        model = Tax
        fields = "__all__"


class BrandSerializer(ModelSerializer):
    
    class Meta:
        model = Brand
        fields = "__all__"



class VehicleModelSerializer(ModelSerializer):
    
    class Meta:
        model = Model
        fields = "__all__" 
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['brand'] = BrandSerializer(instance.brand).data['name']
        # response['tax'] = TaxSerializer(instance.tax).data['rate']
        return response
        

class SparePartModelSerializer(ModelSerializer):
    
    class Meta:
        model = Model
        exclude = ("purchase_price", "retail_price",
                   "wholesale_price", "finance_sale_price", "corporate_sale_price")
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['brand'] = BrandSerializer(instance.brand).data['name']
        return response
        


class VehicleSerializer(ModelSerializer):
    
    class Meta:
        model = Vehicle
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['model'] = VehicleModelSerializer(instance.model).data['name']
        response['brand'] = VehicleModelSerializer(instance.model).data['brand']
        # response['tax'] = TaxSerializer(instance.tax).data['rate']
        return response
        


class SparePartTypeSerializer(ModelSerializer):
  
    class Meta:
        model = SparePartType
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['model'] = SparePartModelSerializer(instance.model).data['name']
        response['brand'] = SparePartModelSerializer(instance.model).data['brand']
        return response



class SparePartSerializer(ModelSerializer):
    
    class Meta:
        model = SparePart
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['part'] = SparePartTypeSerializer(instance.part_type).data['part']
        response['model'] = SparePartTypeSerializer(instance.part_type).data['model']
        response['brand'] = SparePartTypeSerializer(instance.part_type).data['brand']
        return response
        