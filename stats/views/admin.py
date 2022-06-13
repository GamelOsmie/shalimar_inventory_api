from numerize.numerize import numerize
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
            "users": numerize(users),
            "staff": numerize(staff),
            "shipments": numerize(shipments),
            "containers": numerize(containers),
            "warehouses": numerize(warehouses),
            "branches": numerize(branches),
            "spare_parts": numerize(spare_parts),
            "vehicles": numerize(vehicles),
            "service_shops": numerize(service_shops),
            "brands": numerize(brands),
            "models": numerize(models),
            "part_type": numerize(part_type),
        }
        
        return Response(context)
