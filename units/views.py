from cgitb import lookup
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .models import Branch, ServiceShop, Warehouse
from .serializers import BranchSerializer, ServiceShopSerializer, WarehouseSerializer
from rest_framework.filters import SearchFilter


class BranchListView(ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchDetailsView(RetrieveUpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'slug'


class WarehouseListView(ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseDetailsView(RetrieveUpdateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    lookup_field = 'slug'


class ServiceShopListView(ListCreateAPIView):
    queryset = ServiceShop.objects.all()
    serializer_class = ServiceShopSerializer


class ServiceShopDetailsView(RetrieveUpdateAPIView):
    queryset = ServiceShop.objects.all()
    serializer_class = ServiceShopSerializer
    lookup_field = 'slug'
