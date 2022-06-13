from numerize.numerize import numerize
from rest_framework.views import APIView
from rest_framework.response import Response
from operations.models import Shipment

class ShipmentDashboard(APIView):

    def get(self, request):
        instance = Shipment.objects.all()
        
        all_shipments = instance.count()
        pending_departure = instance.filter(on_the_move=False).count()
        pending_arrival = instance.filter(on_the_move=True, container_arrives_at_warehouse__status="no").count()
        arrived = instance.filter(container_arrives_at_warehouse__status="yes").count()
    

        context = {
            "all_shipments": numerize(all_shipments),
            "pending_departure" : numerize(pending_departure),
            "pending_arrival": numerize(pending_arrival),
            "arrived": numerize(arrived),   
        }

        return Response(context)
