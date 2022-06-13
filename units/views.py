from cgitb import lookup
from requests import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .models import Branch, ServiceShop, Warehouse
from .serializers import BranchDetailSerializer, BranchSerializer, ServiceShopDetailSerializer, ServiceShopSerializer, WarehouseDetailSerializer, WarehouseSerializer
from rest_framework.filters import SearchFilter


class BranchListView(ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchDetailsView(RetrieveUpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchDetailSerializer
    lookup_field = 'slug'


class WarehouseListView(ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseDetailsView(RetrieveUpdateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseDetailSerializer
    lookup_field = 'slug'
    
    def get(self, request):
        pass
    
    
    
class WarehouseRetrieveView(APIView):
    
    def get(self, request):
        # print(request)
        
        return Response('return')


class ServiceShopListView(ListCreateAPIView):
    queryset = ServiceShop.objects.all()
    serializer_class = ServiceShopSerializer


class ServiceShopDetailsView(RetrieveUpdateAPIView):
    queryset = ServiceShop.objects.all()
    serializer_class = ServiceShopDetailSerializer
    lookup_field = 'slug'
