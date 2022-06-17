from curses import raw
from rest_framework.response import Response
from rest_framework.generics import  RetrieveAPIView,ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView

from units.models import Branch, Warehouse
from units.serializers import BranchDetailSerializer, WarehouseDetailSerializer
from .models import  BranchSparePartsSupply, BranchVehiclesSupply, CommercialInvoice, ProformaInvoice, Shipment, Container, WarehouseSparePartsSupply, WarehouseVehiclesSupply, WarehouseVehiclesSupply
from .serializers import  BranchSparePartsSupplySerializer, BranchVehiclesSupplySerializer, CommercialInvoiceSerializer, ContainerDetailSerializer, ProformaInvoiceSerializer,  ShipmentListSerializer, ShipmentDetailSerializer, ContainerSerializer, WarehouseSparePartsSupplySerializer, WarehouseVehiclesSupplySerializer
from vehicles.serializers import BrandSerializer, SparePartSerializer, VehicleSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import csv
import datetime
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from vehicles.models import Brand, Model, SparePart, SparePartType, Vehicle
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter


class CustomPaginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000



class CommercialInvoiceListView(ListCreateAPIView):
    queryset = CommercialInvoice.objects.all()
    serializer_class = CommercialInvoiceSerializer
    pagination_class = CustomPaginator
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = (SearchFilter,)
    search_fields = ('invoice_number',)
    # permission_classes = [AdminsOnly]
    

class ProformaInvoiceListView(ListCreateAPIView):
    queryset = ProformaInvoice.objects.all()
    serializer_class = ProformaInvoiceSerializer
    pagination_class = CustomPaginator
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = (SearchFilter,)
    search_fields = ('invoice_number',)
    # permission_classes = [AdminsOnly]
    

class UnlinkedProformaInvoiceListView(ListAPIView):
    queryset = ProformaInvoice.objects.filter(commercial_invoices=None)
    serializer_class = ProformaInvoiceSerializer
    # permission_classes = [AdminsOnly]


class UnlinkedCommercialInvoiceListView(ListAPIView):
    queryset = CommercialInvoice.objects.filter(shipments_commercial_invoices=None)
    serializer_class = CommercialInvoiceSerializer
    # permission_classes = [AdminsOnly]



class ShipmentListView(ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentListSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    search_fields = ('batch_number', 'port_of_origin', 'port_of_destination', 'bill_of_lading_number',
                     'proforma_invoice__invoice_number', 'commercial_invoice__invoice_number')
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


class ContainerListCreateView(ListCreateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    # permission_classes = [AdminsOnly]
       

class AddVehiclesToContainerView(APIView):
    
    def post(self, request):
        # specify where to save the uploaded files
        fs = FileSystemStorage(location='tmp/vehicles/')
          
        # get all vehicle models and part types so you don't hit database multiple times
        models = Model.objects.select_related('brand').all()
        
        # get the uploaded vehicles
        uploaded_vehicles = self.request.FILES.get("vehicles")
        
        # read and save the csv file in memory
        uploaded_vehicles_content = uploaded_vehicles.read()
        vehicles_content = ContentFile(uploaded_vehicles_content)
        vehicles_batch_name = fs.save("_tmp.csv", vehicles_content)
        
        # get the tmp using the batch name
        vehicles_tmp_file = fs.path(vehicles_batch_name)
        
        # open the csv file, read and skip the first row which is the table headers
        vehicles_csv_file = open(vehicles_tmp_file, errors="ignore")
        vehicles_reader = csv.reader(vehicles_csv_file)
        next(vehicles_reader)
        
        # list of vehicles that will be saved
        vehicles_list = []
       
        # list of chassis number and part numbers that will be used to update the list of vehicles in the container
        vehicle_chassis = []

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
            brand_types.append(get_model['brand_id'])

            vehicles_list.append(
                Vehicle(
                    model_id=get_model['id'],
                    chassis_number=chassis_number,
                    engine_number=engine_number,
                    color=color,
                    slug=chassis_number,
                    purchase_price=get_model['purchase_price'],
                    retail_price=get_model['retail_price'],
                    wholesale_price=get_model['wholesale_price'],
                    finance_sale_price=get_model['finance_sale_price'],
                    corporate_sale_price=get_model['corporate_sale_price']
                )
            )
            

        # bulk create the vehicles appended to the vehicles list at once
        Vehicle.objects.bulk_create(vehicles_list)
        
        # this is time to use the chassis number and part numbers saved initially
        # use the chassis_number and part numbers to get all the vehicles and parts you just saved
        vehicles = Vehicle.objects.filter(chassis_number__in=vehicle_chassis)
        

        # serialize the vehicles and spare parts
        serialized_vehicles = VehicleSerializer(vehicles, many=True)
    
        
        # get all th ideas of these vehicles to be saved as vehicles in the container
        vehicle_ids = []


        for vehicle in serialized_vehicles.data:
            vehicle_ids.append(vehicle['id'])

              
        # get the just saved container and store in an instance to so it can be updated
        target_container = Container.objects.get(container_number = request.data['container_number'])
        
        target_container_existing_vehicles = target_container.vehicles.values()
        
        # add existing vehicles to newly added vehicles
        for vehicle in target_container_existing_vehicles:
            vehicle_ids.append(vehicle['id'])
        

        # check if container has mixed content or not
        sorted_brand_type = list(set(brand_types))

        if len(sorted_brand_type) > 1:
            target_container.content_type = "mixed"
    
        else:
            brand = Brand.objects.get(id=sorted_brand_type[0])
            serialized_brand = BrandSerializer(brand, many=False)
            target_container.content_type = serialized_brand.data['name']

        # this is the time to access the saved container and update
        target_container.vehicles.set(vehicle_ids)
        # target_container.spare_parts.set(spare_part_ids)
        target_container.save()

        return Response(serialized_vehicles.data, status=status.HTTP_200_OK)

        
class AddSparePartsToContainerView(APIView):

    def post(self, request):
        # specify where to save the uploaded files
        fs = FileSystemStorage(location='tmp/parts/')

        # get all vehicle models and part types so you don't hit database multiple times
        part_type = SparePartType.objects.all()

        # get the uploaded vehicles
        uploaded_spare_part = self.request.FILES.get("spare_parts")

        # read and save the csv file in memory
        uploaded_spare_part_content = uploaded_spare_part.read()
        spare_part_content = ContentFile(uploaded_spare_part_content)
        spare_part_batch_name = fs.save("_tmp.csv", spare_part_content)

        # get the tmp using the batch name
        spare_part_tmp_file = fs.path(spare_part_batch_name)

        # open the csv file, read and skip the first row which is the table headers
        spare_part_csv_file = open(spare_part_tmp_file, errors="ignore")
        spare_part_reader = csv.reader(spare_part_csv_file)
        next(spare_part_reader)

        # list of vehicles that will be saved
        spare_part_list = []

        # list of chassis number and part numbers that will be used to update the list of vehicles in the container
        spare_part_numbers = []

        
        #go over each row and skip the index using [1], get each role name and save it to update the database
        for row in enumerate(spare_part_reader):

            spare_part_type = row[1][0]
            part_number = row[1][1]
            
            spare_part_numbers.append(part_number)

            # get the specific model and add the id to be saved
            get_part_type = part_type.filter(part=spare_part_type ).values().first()

            spare_part_list.append(
                SparePart(
                    part_type_id=get_part_type['id'],
                    part_number=part_number,
                    slug=part_number,
                    purchase_price=get_part_type['purchase_price'],
                    retail_price=get_part_type['retail_price'],
                    wholesale_price=get_part_type['wholesale_price'],
                    finance_sale_price=get_part_type['finance_sale_price'],
                    corporate_sale_price=get_part_type['corporate_sale_price']
                )
            )

        # bulk create the vehicles appended to the vehicles list at once
        SparePart.objects.bulk_create(spare_part_list)

        # this is time to use the chassis number and part numbers saved initially
        # use the chassis_number and part numbers to get all the vehicles and parts you just saved
        spare_parts = SparePart.objects.filter(
            part_number__in=spare_part_numbers)

        # serialize the vehicles and spare parts
        serialized_spare_parts = SparePartSerializer(spare_parts, many=True)

        # get all th ideas of these vehicles to be saved as vehicles in the container
        spare_part_ids = []

        for part in serialized_spare_parts.data:
            spare_part_ids.append(part['id'])

        # get the just saved container and store in an instance to so it can be updated
        target_container = Container.objects.get(
            container_number=request.data['container_number'])

        target_container_existing_spare_parts = target_container.spare_parts.values()

        # add existing vehicles to newly added vehicles
        for part in target_container_existing_spare_parts:
            spare_part_ids.append(part['id'])


        # this is the time to access the saved container and update
        target_container.spare_parts.set(spare_part_ids)
        target_container.save()

        return Response(serialized_spare_parts.data, status=status.HTTP_200_OK)



class ContainerDetailView(RetrieveUpdateAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerDetailSerializer
    lookup_field = "slug"
    # permission_classes = [AdminsOnly]

   
    
class WarehouseVehiclesSupplyListView(ListCreateAPIView):
    queryset = WarehouseVehiclesSupply.objects.all()
    serializer_class = WarehouseVehiclesSupplySerializer
    
    def perform_create(self, serializer):
        vehicles_supplied_quantity = len(serializer.validated_data['vehicles_supplied'])
        container_id = self.request.data['container']
        
        container = Container.objects.get(id=container_id )
        
        container_vehicles = list(container.vehicles.values())
        vehicles_to_be_supplied = self.request.data['vehicles_supplied']
                
        remaining_vehicles_in_container = []

        for vehicle in container_vehicles:
            if str(vehicle['id']) not in vehicles_to_be_supplied:
                remaining_vehicles_in_container.append(str(vehicle['id']))

        container.vehicles.set(remaining_vehicles_in_container)
        container.save()
        
        return serializer.save(vehicles_supplied_quantity=vehicles_supplied_quantity)


class WarehouseVehiclesSupplyDetailView(RetrieveAPIView):
    queryset =WarehouseVehiclesSupply.objects.all()
    serializer_class = WarehouseVehiclesSupplySerializer
    # permission_classes = [AdminsOnly]
    lookup_field = "slug"
    

    
class WarehouseVehiclesSupplyReceiveView(APIView):
    
    def post(self, request, format=None):
        supply_query =WarehouseVehiclesSupply.objects.get(slug=request.data['supply_slug'])
        
        # save the list of received vehicles and spare parts
        received_vehicles = request.data['vehicles_received']
        
        # get the list of vehicles that exist
        vehicles_in_container = supply_query.vehicles_supplied.values()
        
        
        
        # list of all vehicles and spare parts yet to be received
        vehicles_in_stock = []
       
        # perform a simple check to remove every vehicle and spare part that are lined up to be received
        for vehicle in vehicles_in_container:
            if str(vehicle['id']) not in received_vehicles:
                vehicles_in_stock.append(str(vehicle['id'])) 
                
        
        # update very instance that need update with the most up to date details            
        supply_query.vehicles_supplied.set(vehicles_in_stock)
        supply_query.vehicles_supplied_received = int(supply_query.vehicles_supplied_received) + len(received_vehicles)
        supply_query.received_date = datetime.datetime.now()
        
        
        # save the supply details
        supply_query.save()  
                
               
        # now find the warehouse that is meant to received their products and populate it
        warehouse_query = Warehouse.objects.get(slug=request.data['warehouse_slug'])

       
        # get the list of vehicles and spare parts already available in the warehouse
        warehouse_vehicles_in_stock = list(warehouse_query.vehicles_in_stock.values())
        
        # the list of vehicles in warehouse + new vehicles to be received
        updated_vehicles_in_stock = []
        
        #convert vehicles in stock ids to string to be able to store
        if len(warehouse_vehicles_in_stock) > 0:
            for vehicle in warehouse_vehicles_in_stock:
                updated_vehicles_in_stock.append(str(vehicle['id']))
        
        
        # append newly received vehicles and spare parts to the existing list
        for vehicle in received_vehicles: 
            updated_vehicles_in_stock.append(vehicle)   
 
        
        #update the stock of vehicles and spare parts with the most up to date info
        warehouse_query.vehicles_in_stock.set(updated_vehicles_in_stock)
        
        
        # save warehouse to update the details
        warehouse_query.save()
        
        warehouse_serializer = WarehouseDetailSerializer(warehouse_query, many=False)
        
        
        #update all the vehicles with the latest status
        Vehicle.objects.filter(id__in=vehicles_in_stock).update(current_location="warehouse", custodian=warehouse_serializer.data["name"])
        
            
        return Response(warehouse_serializer.data, status=status.HTTP_201_CREATED)




class WarehouseSparePartsSupplyReceiveView(APIView):

    def post(self, request, format=None):
        supply_query = WarehouseSparePartsSupply.objects.get(
            slug=request.data['supply_slug'])

        # save the list of received vehicles and spare parts
        received_spare_parts = request.data['spare_parts_received']

        # get the list of vehicles that exist
        spare_parts_in_container = supply_query.spare_parts_supplied.values()

        # list of all vehicles and spare parts yet to be received
        spare_parts_in_stock = []

        # perform a simple check to remove every vehicle and spare part that are lined up to be received
        for part in spare_parts_in_container:
            if str(part['id']) not in received_spare_parts:
                spare_parts_in_stock.append(str(part['id']))

        # update very instance that need update with the most up to date details
        supply_query.spare_parts_supplied.set(spare_parts_in_stock)
        supply_query.spare_parts_supplied_received = int(
            supply_query.spare_parts_supplied_received) + len(received_spare_parts)
        supply_query.received_date = datetime.datetime.now()

        # save the supply details
        supply_query.save()

        # now find the warehouse that is meant to received their products and populate it
        warehouse_query = Warehouse.objects.get(
            slug=request.data['warehouse_slug'])

        # get the list of vehicles and spare parts already available in the warehouse
        warehouse_spare_parts_in_stock = list(
            warehouse_query.spare_parts_in_stock.values())

        # the list of vehicles in warehouse + new vehicles to be received
        updated_spare_parts_in_stock = []

        #convert vehicles in stock ids to string to be able to store
        if len(warehouse_spare_parts_in_stock) > 0:
            for part in warehouse_spare_parts_in_stock:
                updated_spare_parts_in_stock.append(str(part['id']))

        # append newly received vehicles and spare parts to the existing list
        for part in received_spare_parts:
            updated_spare_parts_in_stock.append(part)

        #update the stock of vehicles and spare parts with the most up to date info
        warehouse_query.spare_parts_in_stock.set(updated_spare_parts_in_stock)

        # save warehouse to update the details
        warehouse_query.save()

        warehouse_serializer = WarehouseDetailSerializer(
            warehouse_query, many=False)

        #update all the vehicles with the latest status
        SparePart.objects.filter(id__in=spare_parts_in_stock).update(
            current_location="warehouse", custodian=warehouse_serializer.data["name"])

        return Response(warehouse_serializer.data, status=status.HTTP_201_CREATED)




class WarehouseSparePartsSupplyListView(ListCreateAPIView):
    queryset = WarehouseSparePartsSupply.objects.all()
    serializer_class = WarehouseSparePartsSupplySerializer

    def perform_create(self, serializer):
        spare_part_supplied_quantity = len(
            serializer.validated_data['spare_parts_supplied'])
        container_id = self.request.data['container']

        container = Container.objects.get(id=container_id)

        container_spare_parts = list(container.spare_parts.values())
        spare_part_to_be_supplied = self.request.data['spare_parts_supplied']
        
        remaining_spare_part_in_container = []

        for part in container_spare_parts:
            if str(part['id']) not in spare_part_to_be_supplied:
                remaining_spare_part_in_container.append(str(part['id']))

        container.spare_parts.set(remaining_spare_part_in_container)
        container.save()

        return serializer.save(spare_parts_supplied_quantity=spare_part_supplied_quantity)



class WarehouseSparePartsSupplyDetailView(RetrieveAPIView):
    queryset = WarehouseSparePartsSupply.objects.all()
    serializer_class = WarehouseSparePartsSupplySerializer
    # permission_classes = [AdminsOnly]
    lookup_field = "slug"



class BranchVehiclesSupplyListView(ListCreateAPIView):
    queryset = BranchVehiclesSupply.objects.all()
    serializer_class = BranchVehiclesSupplySerializer

    def perform_create(self, serializer):
        vehicles_supplied_quantity = len(
            serializer.validated_data['vehicles_supplied'])
        warehouse_id = self.request.data['warehouse']

        warehouse = Warehouse.objects.get(id=warehouse_id)

        warehouse_vehicles = list(warehouse.vehicles_in_stock.values())
        vehicles_to_be_supplied = self.request.data['vehicles_supplied']

        remaining_vehicles_in_warehouse = []

        for vehicle in warehouse_vehicles:
            if str(vehicle['id']) not in vehicles_to_be_supplied:
                remaining_vehicles_in_warehouse.append(str(vehicle['id']))

        warehouse.vehicles_in_stock.set(remaining_vehicles_in_warehouse)
        warehouse.save()

        return serializer.save(vehicles_supplied_quantity=vehicles_supplied_quantity)


class BranchVehiclesSupplyDetailView(RetrieveAPIView):
    queryset = BranchVehiclesSupply.objects.all()
    serializer_class = BranchVehiclesSupplySerializer
    # permission_classes = [AdminsOnly]
    lookup_field = "slug"
    
    
class BranchVehiclesSupplyReceiveView(APIView):

    def post(self, request, format=None):
        supply_query = BranchVehiclesSupply.objects.get(
            slug=request.data['supply_slug'])

        # save the list of received vehicles and spare parts
        received_vehicles = request.data['vehicles_received']

        # get the list of vehicles that exist
        vehicles_in_warehouse = supply_query.vehicles_supplied.values()

        # list of all vehicles and spare parts yet to be received
        vehicles_in_stock = []

        # perform a simple check to remove every vehicle and spare part that are lined up to be received
        for vehicle in vehicles_in_warehouse:
            if str(vehicle['id']) not in received_vehicles:
                vehicles_in_stock.append(str(vehicle['id']))

        # update very instance that need update with the most up to date details
        supply_query.vehicles_supplied.set(vehicles_in_stock)
        supply_query.vehicles_supplied_received = int(
            supply_query.vehicles_supplied_received) + len(received_vehicles)
        supply_query.received_date = datetime.datetime.now()

        # save the supply details
        supply_query.save()

        # now find the warehouse that is meant to received their products and populate it
        branch_query = Branch.objects.get(
            slug=request.data['branch_slug'])

        # get the list of vehicles and spare parts already available in the warehouse
        branch_vehicles_in_stock = list(
            branch_query.vehicles_in_stock.values())

        # the list of vehicles in warehouse + new vehicles to be received
        updated_vehicles_in_stock = []

        #convert vehicles in stock ids to string to be able to store
        if len(branch_vehicles_in_stock) > 0:
            for vehicle in branch_vehicles_in_stock:
                updated_vehicles_in_stock.append(str(vehicle['id']))

        # append newly received vehicles and spare parts to the existing list
        for vehicle in received_vehicles:
            updated_vehicles_in_stock.append(vehicle)

        #update the stock of vehicles and spare parts with the most up to date info
        branch_query.vehicles_in_stock.set(updated_vehicles_in_stock)

        # save warehouse to update the details
        branch_query.save()

        branch_serializer = BranchDetailSerializer(
            branch_query, many=False)

        #update all the vehicles with the latest status
        Vehicle.objects.filter(id__in=vehicles_in_stock).update(
            current_location="branch", custodian=branch_serializer.data["name"])

        return Response(branch_serializer.data, status=status.HTTP_201_CREATED)



class BranchSparePartsSupplyListView(ListCreateAPIView):
    queryset = BranchSparePartsSupply.objects.all()
    serializer_class = BranchSparePartsSupplySerializer

    def perform_create(self, serializer):
        spare_parts_supplied_quantity = len(
            serializer.validated_data['spare_parts_supplied'])
        warehouse_id = self.request.data['warehouse']

        warehouse = Warehouse.objects.get(id=warehouse_id)

        warehouse_spare_parts = list(warehouse.spare_parts_in_stock.values())
        spare_parts_to_be_supplied = self.request.data['spare_parts_supplied']

        remaining_spare_parts_in_warehouse = []

        for part in warehouse_spare_parts:
            if str(part['id']) not in spare_parts_to_be_supplied:
                remaining_spare_parts_in_warehouse.append(str(part['id']))

        warehouse.spare_parts_in_stock.set(remaining_spare_parts_in_warehouse)
        warehouse.save()

        return serializer.save(spare_parts_supplied_quantity=spare_parts_supplied_quantity)


class BranchSparePartsSupplyDetailView(RetrieveAPIView):
    queryset = BranchSparePartsSupply.objects.all()
    serializer_class = BranchSparePartsSupplySerializer
    # permission_classes = [AdminsOnly]
    lookup_field = "slug"


class BranchSparePartsSupplyReceiveView(APIView):

    def post(self, request, format=None):
        supply_query = BranchSparePartsSupply.objects.get(
            slug=request.data['supply_slug'])

        # save the list of received vehicles and spare parts
        received_spare_parts = request.data['spare_parts_received']

        # get the list of vehicles that exist
        spare_parts_in_warehouse = supply_query.spare_parts_supplied.values()

        # list of all vehicles and spare parts yet to be received
        spare_parts_in_stock = []

        # perform a simple check to remove every vehicle and spare part that are lined up to be received
        for part in spare_parts_in_warehouse:
            if str(part['id']) not in received_spare_parts:
                spare_parts_in_stock.append(str(part['id']))

        # update very instance that need update with the most up to date details
        supply_query.spare_parts_supplied.set(spare_parts_in_stock)
        supply_query.spare_parts_supplied_received = int(
            supply_query.spare_parts_supplied_received) + len(received_spare_parts)
        supply_query.received_date = datetime.datetime.now()

        # save the supply details
        supply_query.save()

        # now find the warehouse that is meant to received their products and populate it
        branch_query = Branch.objects.get(
            slug=request.data['branch_slug'])

        # get the list of vehicles and spare parts already available in the warehouse
        branch_spare_parts_in_stock = list(
            branch_query.spare_parts_in_stock.values())

        # the list of vehicles in warehouse + new vehicles to be received
        updated_spare_parts_in_stock = []

        #convert vehicles in stock ids to string to be able to store
        if len(branch_spare_parts_in_stock) > 0:
            for part in branch_spare_parts_in_stock:
                updated_spare_parts_in_stock.append(str(part['id']))

        # append newly received vehicles and spare parts to the existing list
        for part in received_spare_parts:
            updated_spare_parts_in_stock.append(part)

        #update the stock of vehicles and spare parts with the most up to date info
        branch_query.spare_parts_in_stock.set(updated_spare_parts_in_stock)

        # save warehouse to update the details
        branch_query.save()

        branch_serializer = BranchDetailSerializer(
            branch_query, many=False)

        #update all the vehicles with the latest status
        SparePart.objects.filter(id__in=spare_parts_in_stock).update(
            current_location="branch", custodian=branch_serializer.data["name"])

        return Response(branch_serializer.data, status=status.HTTP_201_CREATED)




class UpdateWarehouseMissingVehicles(APIView):
    
    def post(self, request):
        warehouse_id = request.data['warehouse']
        warehouse = Warehouse.objects.get(id=warehouse_id)
        
        vehicles_in_stock = request.data['vehicles_in_stock']
        vehicles_missing = request.data['vehicles_missing']
        
        
        warehouse.vehicles_in_stock.set(vehicles_in_stock)
        warehouse.vehicles_missing.set(vehicles_missing)
        
        warehouse.save()
        
        warehouse.vehicles_missing_count = len(vehicles_missing)
        warehouse.vehicles_in_stock_count = len(vehicles_in_stock)
        
        serializer = WarehouseDetailSerializer(warehouse, many=False)
        
        Vehicle.objects.filter(id__in=vehicles_in_stock).update(current_location="warehouse")
        Vehicle.objects.filter(id__in=vehicles_missing).update(current_location="missing")
        
        return Response(serializer.data)



class UpdateBranchMissingVehicles(APIView):

    def post(self, request):
        branch_id = request.data['branch']
        branch = Branch.objects.get(id=branch_id)

        vehicles_in_stock = request.data['vehicles_in_stock']
        vehicles_missing = request.data['vehicles_missing']

        branch.vehicles_in_stock.set(vehicles_in_stock)
        branch.vehicles_missing.set(vehicles_missing)

        branch.save()

        branch.vehicles_missing_count = len(vehicles_missing)
        branch.vehicles_in_stock_count = len(vehicles_in_stock)

        serializer = WarehouseDetailSerializer(branch, many=False)

        Vehicle.objects.filter(id__in=vehicles_in_stock).update(
            current_location="branch")
        Vehicle.objects.filter(id__in=vehicles_missing).update(
            current_location="missing")

        return Response(serializer.data)
    


class UpdateWarehouseMissingSpareParts(APIView):
    
    def post(self, request):
        warehouse_id = request.data['warehouse']
        warehouse = Warehouse.objects.get(id=warehouse_id)
        
        spare_parts_in_stock = request.data['spare_parts_in_stock']
        spare_parts_missing = request.data['spare_parts_missing']
        
        
        warehouse.spare_parts_in_stock.set(spare_parts_in_stock)
        warehouse.spare_parts_missing.set(spare_parts_missing)
        
        warehouse.save()
        
        warehouse.spare_part_missing_count = len(spare_parts_missing)
        warehouse.spare_part_in_stock_count = len(spare_parts_in_stock)
        
        serializer = WarehouseDetailSerializer(warehouse, many=False)
        
        SparePart.objects.filter(id__in=spare_parts_in_stock).update(current_location="warehouse")
        SparePart.objects.filter(id__in=spare_parts_missing).update(current_location="missing")
        
        return Response(serializer.data)



class UpdateBranchMissingSpareParts(APIView):
    
    def post(self, request):
        branch_id = request.data['branch']
        branch = Branch.objects.get(id=branch_id)
        
        spare_parts_in_stock = request.data['spare_parts_in_stock']
        spare_parts_missing = request.data['spare_parts_missing']
        
        
        branch.spare_parts_in_stock.set(spare_parts_in_stock)
        branch.spare_parts_missing.set(spare_parts_missing)
        
        branch.save()
        
        branch.spare_part_missing_count = len(spare_parts_missing)
        branch.spare_part_in_stock_count = len(spare_parts_in_stock)
        
        serializer = WarehouseDetailSerializer(branch, many=False)
        
        SparePart.objects.filter(id__in=spare_parts_in_stock).update(current_location="branch")
        SparePart.objects.filter(id__in=spare_parts_missing).update(current_location="missing")
        
        return Response(serializer.data)




class UpdateWarehouseDamagedVehicles(APIView):
    
    def post(self, request):
        warehouse_id = request.data['warehouse']
        warehouse = Warehouse.objects.get(id=warehouse_id)
        
        vehicles_in_stock = request.data['vehicles_in_stock']
        vehicles_damaged = request.data['vehicles_damaged']
        
        
        warehouse.vehicles_in_stock.set(vehicles_in_stock)
        warehouse.vehicles_damaged.set(vehicles_damaged)
        
        warehouse.save()
        
        warehouse.vehicles_damaged_count = len(vehicles_damaged)
        warehouse.vehicles_in_stock_count = len(vehicles_in_stock)
        
        serializer = WarehouseDetailSerializer(warehouse, many=False)
        
        Vehicle.objects.filter(id__in=vehicles_in_stock).update(current_location="warehouse")
        Vehicle.objects.filter(id__in=vehicles_damaged).update(current_location="damaged")
        
        return Response(serializer.data)



class UpdateBranchDamagedVehicles(APIView):

    def post(self, request):
        branch_id = request.data['branch']
        branch = Branch.objects.get(id=branch_id)

        vehicles_in_stock = request.data['vehicles_in_stock']
        vehicles_damaged = request.data['vehicles_damaged']

        branch.vehicles_in_stock.set(vehicles_in_stock)
        branch.vehicles_damaged.set(vehicles_damaged)

        branch.save()

        branch.vehicles_damaged_count = len(vehicles_damaged)
        branch.vehicles_in_stock_count = len(vehicles_in_stock)

        serializer = WarehouseDetailSerializer(branch, many=False)

        Vehicle.objects.filter(id__in=vehicles_in_stock).update(current_location="branch")
        Vehicle.objects.filter(id__in=vehicles_damaged).update(current_location="damaged")

        return Response(serializer.data)



class UpdateWarehouseDamagedSpareParts(APIView):
    
    def post(self, request):
        warehouse_id = request.data['warehouse']
        warehouse = Warehouse.objects.get(id=warehouse_id)
        
        spare_parts_in_stock = request.data['spare_parts_in_stock']
        spare_parts_damaged = request.data['spare_parts_damaged']
        
        
        warehouse.spare_parts_in_stock.set(spare_parts_in_stock)
        warehouse.spare_parts_damaged.set(spare_parts_damaged)
        
        warehouse.save()
        
        warehouse.spare_part_damaged_count = len(spare_parts_damaged)
        warehouse.spare_part_in_stock_count = len(spare_parts_in_stock)
        
        serializer = WarehouseDetailSerializer(warehouse, many=False)
        
        SparePart.objects.filter(id__in=spare_parts_in_stock).update(current_location="warehouse")
        SparePart.objects.filter(id__in=spare_parts_damaged).update(current_location="damaged")
        
        return Response(serializer.data)



class UpdateBranchDamagedSpareParts(APIView):
    
    def post(self, request):
        branch_id = request.data['branch']
        branch = Branch.objects.get(id=branch_id)
        
        spare_parts_in_stock = request.data['spare_parts_in_stock']
        spare_parts_damaged = request.data['spare_parts_damaged']
        
        
        branch.spare_parts_in_stock.set(spare_parts_in_stock)
        branch.spare_parts_damaged.set(spare_parts_damaged)
        
        branch.save()
        
        branch.spare_part_damaged_count = len(spare_parts_damaged)
        branch.spare_part_in_stock_count = len(spare_parts_in_stock)
        
        serializer = WarehouseDetailSerializer(branch, many=False)
        
        SparePart.objects.filter(id__in=spare_parts_in_stock).update(current_location="branch")
        SparePart.objects.filter(id__in=spare_parts_damaged).update(current_location="damaged")
        
        return Response(serializer.data)
