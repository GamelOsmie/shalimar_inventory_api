from rest_framework.response import Response
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
    
    
class BranchRetrieveView(APIView):

    def get(self, request):
        specific_branch_slug = request.GET.get('slug')
        user_role = request.user.role
        user_workplace = request.user.workplace
        serializer = ""

        if user_role == "Super Admin" or user_role == "Admin":
            branch = Branch.objects.get(slug=specific_branch_slug)
            serializer = BranchDetailSerializer(branch, many=False)
            

        if user_role == "Branch Officer":
            branch = Branch.objects.get(name=user_workplace)
            serializer = BranchDetailSerializer(branch, many=False)

        return Response(serializer.data)



class WarehouseListView(ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseDetailsView(RetrieveUpdateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseDetailSerializer
    lookup_field = 'slug'


class WarehouseRetrieveView(APIView):
    
    def get(self, request):
        specific_warehouse_slug = request.GET.get('slug')
        user_role = request.user.role
        user_workplace = request.user.workplace
        serializer = ""
        
        if user_role == "Super Admin" or user_role == "Admin":
            warehouse = Warehouse.objects.get(slug=specific_warehouse_slug)
            serializer = WarehouseDetailSerializer(warehouse, many=False)

           
        if user_role == "Warehouse Officer":
            warehouse = Warehouse.objects.get(name=user_workplace)
            serializer = WarehouseDetailSerializer(warehouse, many=False)
            
        
        return Response(serializer.data)
        
        
        

class ServiceShopListView(ListCreateAPIView):
    queryset = ServiceShop.objects.all()
    serializer_class = ServiceShopSerializer


class ServiceShopDetailsView(RetrieveUpdateAPIView):
    queryset = ServiceShop.objects.all()
    serializer_class = ServiceShopDetailSerializer
    lookup_field = 'slug'
