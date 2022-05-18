from rest_framework.serializers import ModelSerializer
from .models import *


class BranchSerializer(ModelSerializer):

    class Meta:
        model = Branch
        fields = "__all__"
        

class WarehouseSerializer(ModelSerializer):

    class Meta:
        model = Warehouse
        fields = "__all__"
        

class ServiceShopSerializer(ModelSerializer):

    class Meta:
        model = ServiceShop
        fields = "__all__"
