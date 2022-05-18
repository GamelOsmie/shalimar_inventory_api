from tabnanny import check
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView,ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from .models import  BranchOperation, CommercialInvoice, ProformaInvoice, ServiceShopOperation, Shipment, Container, WareSupply, WarehouseOperation
from .serializers import  BranchOperationSerializer, CommercialInvoiceSerializer, ProformaInvoiceSerializer, ServiceShopOperationSerializer, ShipmentListSerializer, ShipmentDetailSerializer, ContainerSerializer, WarehouseOperationSerializer, WarehouseSupplySerializer
from vehicles.serializers import BrandSerializer, SparePartSerializer, VehicleSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import csv
import datetime
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from vehicles.models import Brand, Model, SparePart, SparePartType, Vehicle


class CommercialInvoiceListView(ListCreateAPIView):
    queryset = CommercialInvoice.objects.all()
    serializer_class = CommercialInvoiceSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [AdminsOnly]
    


class ProformaInvoiceListView(ListCreateAPIView):
    queryset = ProformaInvoice.objects.all()
    serializer_class = ProformaInvoiceSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [AdminsOnly]



class ShipmentListView(ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentListSerializer
    # permission_classes = [AdminsOnly]
    
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            self.serializer_class = ShipmentDetailSerializer
        return self.serializer_class
    

class ShipmentDetailView(RetrieveUpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentDetailSerializer
    lookup_field = "slug"
    # permission_classes = [AdminsOnly]


class ContainerListView(ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    # permission_classes = [AdminsOnly]
    
    
class ContainerCreateView(APIView):

    def post(self, request):
        # specify where to save the uploaded files
        fs = FileSystemStorage(location='tmp/')
        
        # create a container instance and save. this will be updated with vehicles and spare parts later
        container = Container(
            container_number = request.data['container_number']
        )
        container.save()


        #get all vehicle models and part types so you don't hit database multiple times
        models = Model.objects.all()
        part_type = SparePartType.objects.all()
        
        
        # get the just saved container and store in an instance to so it can be updated
        saved_container = Container.objects.get(container_number = request.data['container_number'])
        
        # get the uploaded vehicles and spareparts
        uploaded_vehicles = self.request.FILES.get("vehicles")
        uploaded_spare_parts = self.request.FILES.get("spare_parts")


        # read and save the csv file in memory
        uploaded_vehicles_content = uploaded_vehicles.read()
        vehicles_content = ContentFile(uploaded_vehicles_content)
        vehicles_batch_name = fs.save(
            "_tmp.csv", vehicles_content
        )
        
        uploaded_spare_parts_content = uploaded_spare_parts.read()
        spare_parts_content = ContentFile(uploaded_spare_parts_content)
        spare_parts_batch_name = fs.save(
            "_tmp.csv", spare_parts_content
        )

        
        # get the tmp using the batch name
        vehicles_tmp_file = fs.path(vehicles_batch_name)
        spare_parts_tmp_file = fs.path(spare_parts_batch_name)

        # open the csv file, read and skip the first row which is the table headers
        vehicles_csv_file = open(vehicles_tmp_file, errors="ignore")
        vehicles_reader = csv.reader(vehicles_csv_file)
        next(vehicles_reader)
        
        spare_parts_csv_file = open(spare_parts_tmp_file, errors="ignore")
        spare_parts_reader = csv.reader(spare_parts_csv_file)
        next(spare_parts_reader)

        # list of vehicles that will be saved
        vehicles_list = []
        spare_parts_list = []
        
        # list of chassis number and part numbers that will be used to update the list of vehicles in the container
        vehicle_chassis = []
        spare_part_numbers = []
        
        # brand types to determine if the vehicle has mixed content or not
        brand_types = []
        
        #go over each row and skip the index using [1], get each role name and save it to update the database
        for row in enumerate(vehicles_reader):
                                    
                                    
            model = row[1][0]
            chassis_number = row[1][1]
            engine_number = row[1][2]
            color = row[1][3]
            
            vehicle_chassis.append(chassis_number)
            
            # get the specific model and add the id to be saved
            get_model = models.filter(name=model).values().first()
            brand_types.append(get_model['brand'])
            
            vehicles_list.append(
                Vehicle(
                    model_id=get_model['id'],
                    chassis_number=chassis_number,
                    engine_number=engine_number,
                    color=color,
                    slug=chassis_number
                )
            )
        
        # go over the spare parts to save it
        for row in enumerate(spare_parts_reader):

            part_number = row[1][0]
            part_type = row[1][1]
           
            spare_part_numbers.append(part_number)

            # get the specific model and add the id to be saved
            get_part_type = SparePartType.filter(part=part_type).values().first()

            
            spare_parts_list.append(
                SparePart(
                    part_type_id=get_part_type['id'],
                    part_number=part_number,
                )
            )
          
        
        # bulk create the vehicles appended to the vehicles list at once    
        Vehicle.objects.bulk_create(vehicles_list)
        SparePart.objects.bulk_create(spare_parts_list)
                
        # this is time to use the chassis number and part numbers saved initially
        # use the chassis_number and part numbers to get all the vehicles and parts you just saved         
        vehicles = Vehicle.objects.filter(chassis_number__in=vehicle_chassis)
        spare_parts = SparePart.objects.filter(part_number__in=spare_part_numbers)
        
        # serialize the vehicles and spare parts
        serialized_vehicles = VehicleSerializer(vehicles, many=True)
        serialized_spare_parts = SparePartSerializer(spare_parts, many=True)
        
        # get all th ideas of these vehicles to be saved as vehicles in the container
        vehicle_ids = []
        spare_part_ids = []
        
        for vehicle in serialized_vehicles.data:
            vehicle_ids.append(vehicle['id'])
        
        for spare_part in serialized_spare_parts.data:
            spare_part_ids.append(spare_part['id'])
            
        # check if container has mixed content or not
        
        
        
        sorted_brand_type = list(set(brand_types))
            
        if len(sorted_brand_type) > 1:
            saved_container.content_type = "mixed"
        else:
            brand = Brand.objects.get(id=sorted_brand_type[0])
            serialized_brand = BrandSerializer(brand, many=False)
            saved_container.content_type = serialized_brand.data['name']
            
        # this is the time to access the saved container and update
        saved_container.shipment_batch = Shipment.objects.get(id=request.data['shipment_batch'])
        saved_container.vehicles.set(vehicle_ids)
        saved_container.spare_parts.set(spare_part_ids)
        saved_container.save()
        
        
        return Response("You have successfully added a container to shipment", status=status.HTTP_200_OK)



class ContainerDetailView(RetrieveUpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentDetailSerializer
    look_field = "slug"
    # permission_classes = [AdminsOnly]


class BranchOperationsListView(ListCreateAPIView):
    queryset = BranchOperation.objects.all()
    serializer_class = BranchOperationSerializer
    # permission_classes = [AdminsOnly]
    

class BranchOperationsDetailView(RetrieveUpdateAPIView):
    queryset = BranchOperation.objects.all()
    serializer_class = BranchOperationSerializer
    # permission_classes = [AdminsOnly]
    lookup_field = "id"


class WarehouseOperationsListView(ListAPIView):
    queryset = WarehouseOperation.objects.all()
    serializer_class = WarehouseOperationSerializer
    # permission_classes = [AdminsOnly]
    

class WarehouseOperationsDetailView(RetrieveUpdateAPIView):
    queryset = WarehouseOperation.objects.all()
    serializer_class = WarehouseOperationSerializer
    # permission_classes = [AdminsOnly]
    lookup_field = "id"
    
    


class ServiceShopOperationsListView(ListAPIView):
    queryset = ServiceShopOperation.objects.all()
    serializer_class = ServiceShopOperationSerializer
    # permission_classes = [AdminsOnly]
    

class ServiceShopOperationsDetailView(RetrieveUpdateAPIView):
    queryset = ServiceShopOperation.objects.all()
    serializer_class = ServiceShopOperationSerializer
    # permission_classes = [AdminsOnly]
    lookup_field = "id"
    
    
    
class WarehouseSupplyListView(ListAPIView):
    queryset =  WareSupply.objects.all()
    serializer_class = WarehouseSupplySerializer
    
    def perform_create(self, serializer):
        vehicles_supplied_quantity = serializer.data['vehicles_supplied'].count()
        spare_parts_supplied_quantity = serializer.data['spare_parts_supplied'].count()
        
        return serializer.save(vehicles_supplied_quantity=vehicles_supplied_quantity, spare_parts_supplied_quantity=spare_parts_supplied_quantity)


class WarehouseSupplyDetailView(RetrieveAPIView):
    queryset = WareSupply.objects.all()
    serializer_class = WarehouseSupplySerializer
    # permission_classes = [AdminsOnly]
    lookup_field = "slug"
    

    
class WarehouseSupplyReceiveView(APIView):
    
    def post(self, request):
        supply_query = WareSupply.objects.get(slug=request.data['slug'])
        
    
        # save the list of received vehicles and spare parts
        received_vehicles = request.data['vehicles_received']
        received_spare_parts = request.data['spare_parts_received']
        
        # get the list of spare parts and vehicles that exist
        vehicles_in_container = supply_query.vehicles_supplied.values()
        spare_parts_in_container = supply_query.spare_parts_supplied.values()
        
        # list of all vehicles and spare parts yet to be received
        vehicles_in_stock = []
        spare_parts_in_stock = []
        
        # perform a simple check to remove every vehicle and spare part that are lined up to be received
        for vehicle in vehicles_in_container:
            if vehicle['id'] not in received_vehicles:
                vehicles_in_stock.append(vehicle['id']) 
                
        
        for spare_part in spare_parts_in_container:
            if spare_part['id'] not in received_spare_parts:
                spare_parts_in_stock.append(spare_part['id']) 
                
        # update very instance that need update with the most up to date details            
        supply_query.vehicles_supplied = vehicles_in_stock
        supply_query.vehicles_supplied = received_vehicles.count()
        supply_query.spare_parts_supplied = spare_parts_in_stock
        supply_query.spare_parts_supplied = received_spare_parts.count()
        supply_query.received_date = datetime.datetime.now()
        
        # save the supply details
        supply_query.save()
        
        # now find the warehouse that is meant to received their products and populate it
        warehouse_query = WarehouseOperation.objects.get(id=request.data['id'])
        
        # get the list of vehicles and spare parts already available in the warehouse
        warehouse_vehicles_in_stock = list(warehouse_query.vehicles_in_stock.values())
        warehouse_spare_parts_in_stock = list(warehouse_query.spare_parts_in_stock.values())
        
        # append newly received vehicles and spare parts to the existing list 
        warehouse_vehicles_in_stock.append(received_vehicles)
        warehouse_spare_parts_in_stock.append(received_spare_parts)
        
        # update the stock of vehicles and spare parts with the most up to date info
        warehouse_query.vehicles_in_stock.set(warehouse_vehicles_in_stock)
        warehouse_query.spare_parts_in_stock.set(warehouse_spare_parts_in_stock)
        
        # save warehouse to update the details
        warehouse_query.save()
        
            
        return Response({"supply received successfully"}, status=status.HTTP_200_OK)

        
    
