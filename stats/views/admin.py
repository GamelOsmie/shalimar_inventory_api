from rest_framework.views import APIView
from rest_framework.response import Response
from operations.models import Container, Shipment

from staff.models import Staff
from units.models import Branch, ServiceShop, Warehouse
from users.models import User
from vehicles.models import Brand, Model, SparePart, SparePartType, Vehicle


class DashboardSummary(APIView):
    
    def get(self, request):
        staff = Staff.objects.all().count()
        users = User.objects.all().exclude(role="Super Admin").count()
        warehouses = Warehouse.objects.all().count()
        branches = Branch.objects.all().count()
        service_shops = ServiceShop.objects.all().count()
        spare_parts = SparePart.objects.all().count()
        vehicles = Vehicle.objects.all().count()
        shipments = Shipment.objects.all().count()
        containers = Container.objects.all().count()
        brands = Brand.objects.all().count()
        models = Model.objects.all().count()
        part_type = SparePartType.objects.all().count()
        
        
        context = {
            "users": users,
            "staff": staff,
            "shipments": shipments,
            "containers": containers,
            "warehouses": warehouses,
            "branches": branches,
            "spare_parts": spare_parts,
            "vehicles": vehicles,
            "service_shops": service_shops,
            "brands": brands,
            "models": models,
            "part_type": part_type,
        }
        
        return Response(context)
