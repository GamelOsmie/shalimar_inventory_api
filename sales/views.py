from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from sales.models import Customer, FinanceAndCorporateSale, Organization, Retail, Wholesale
from sales.serializer import CustomerSerializer, FinanceAndCorporateSaleSerializer, OrganizationSerializer, RetailSerializer, WholesaleSerializer
from units.models import Branch, Warehouse
from units.serializers import BranchDetailSerializer, WarehouseDetailSerializer
from vehicles.models import SparePart, Vehicle


class CustomPaginator(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000



class RetailCustomersListView(ListAPIView):
    queryset = Customer.objects.filter(customer_type="retail")
    serializer_class = CustomerSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    search_fields = ('first_name', 'middle_name', 'last_name', 'phone_number', 'email')


class WholesaleCustomersListView(ListAPIView):
    queryset = Customer.objects.filter(customer_type="wholesale")
    serializer_class = CustomerSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    search_fields = ('first_name', 'middle_name', 'last_name', 'phone_number', 'email')
   

class CustomersDetailView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "id"



class FinanceSaleOrganizationListView(ListAPIView):
    queryset = Organization.objects.filter(consumption_type="finance sale")
    serializer_class = OrganizationSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    search_fields = ('name', 'location', 'address','phone_number', 'email')
   


class CorporateSaleOrganizationListView(ListAPIView):
    queryset = Organization.objects.filter(consumption_type="corporate sale")
    serializer_class = OrganizationSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    search_fields = ('name', 'location', 'address','phone_number', 'email')
   


class OrganizationsDetailView(RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "id"
   


class RetailListView(ListAPIView):
    queryset = Retail.objects.all()
    serializer_class = RetailSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    search_fields = ('invoice_number','branch__name', 'branch__location', 'customer__first_name', 'customer__middle_name', 'customer__last_name', 'customer__phone_number', 'customer__email')
    
    def get_queryset(self):
        
        if self.request.user.role is "Retail Officer":
            return Retail.objects.filter(branch__name=self.request.user.workplace)        
        
        return super().get_queryset()
    
    
class RetailDetailView(RetrieveAPIView):
    queryset = Retail.objects.all()
    serializer_class = RetailSerializer
    lookup_field = "slug"
   
   
class RetailPurchaseView(APIView):
    
    def post(self, request):
        # get all inputs from user
        branch_id = request.data['branch']
        vehicles_purchased = request.data['vehicles_sold']
        spare_parts_purchased = request.data['spare_parts_sold']
        tax = int(request.data['tax']) / 100
        discount = int(request.data['discount']) / 100
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        middle_name = request.data['middle_name']
        
    
        # set the customer id to global
        global customer_id
        
        # get the purchase brand with the branch id
        branch = Branch.objects.get(id=branch_id)
        
        # get or create a user that made the purchase if they dont exist
        customer, created = Customer.objects.get_or_create(first_name = request.data['first_name'], last_name = request.data['last_name'], phone_number = request.data['phone_number'], defaults={'email': request.data['email'], 'middle_name': middle_name, 'customer_type':'retail'})
     
        # grab the id from existing or new customer                
        if created:
            newly_created_customer = Customer.objects.get(first_name = first_name, last_name = last_name, phone_number = request.data['phone_number'])
            customer_id = str(newly_created_customer.id)
        else:
            customer_id = str(customer.id)
            
        # set customer to buyer to create a retail sale
        buyer = Customer.objects.get(id=customer_id)
        
        # save new retail sale                    
        retail = Retail(branch= branch, customer=buyer, tax = tax, discount = discount)
        retail.save()
        
        # add spare parts and vehicles to the sale
        for vehicle in vehicles_purchased:
            retail.vehicles_sold.add(vehicle)
        
        for part in spare_parts_purchased:
            retail.spare_parts_sold.add(part)
        
        
        # get the list of vehicles that exist
        vehicles_in_branch = branch.vehicles_in_stock.values()
        spare_parts_in_branch = branch.spare_parts_in_stock.values()

        # list of all vehicles and spare parts yet to be received
        vehicles_in_stock = []
        spare_parts_in_stock = []

        # perform a simple check to remove every vehicle and spare part that are lined up to be received
        for vehicle in vehicles_in_branch:
            if str(vehicle['id']) not in vehicles_purchased:
                vehicles_in_stock.append(str(vehicle['id']))
        
        
        for part in spare_parts_in_branch:
            if str(part['id']) not in spare_parts_purchased:
                spare_parts_in_stock.append(str(part['id']))
                

        # sale remaining vehicle and spare parts to the shop
        branch.vehicles_in_stock.set(vehicles_in_stock)
        branch.spare_parts_in_stock.set(spare_parts_in_stock)
        branch.save()
                        
        # serialize the branch as response
        branch_serializer = BranchDetailSerializer(
            branch, many=False)

        #update all the vehicles with the latest status
        Vehicle.objects.filter(id__in=vehicles_purchased).update(
            current_location="retail", custodian=f"{first_name} {middle_name} {last_name}")

        #update all the vehicles with the latest status
        SparePart.objects.filter(id__in=spare_parts_purchased).update(
            current_location="retail", custodian=f"{first_name} {middle_name} {last_name}")

        return Response(branch_serializer.data , status=status.HTTP_201_CREATED)

            

        
        
   

class WholesaleListView(ListAPIView):
    queryset = Wholesale.objects.all()
    serializer_class = WholesaleSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    search_fields = ('invoice_number','warehouse__name', 'warehouse__location', 'customer__first_name', 'customer__middle_name', 'customer__last_name', 'customer__phone_number', 'customer__email')
    
   
    def get_queryset(self):

        if self.request.user.role is "Warehouse Officer":
            return Wholesale.objects.filter(warehouse__name=self.request.user.workplace)

        return super().get_queryset()
    
 
  
class WholesaleDetailView(RetrieveAPIView):
    queryset = Wholesale.objects.all()
    serializer_class = WholesaleSerializer
    lookup_field = "slug"


class WholesaleView(APIView):

    def post(self, request):
        # get all inputs from user
        warehouse_id = request.data['warehouse']
        vehicles_purchased = request.data['vehicles_sold']
        spare_parts_purchased = request.data['spare_parts_sold']
        tax = int(request.data['tax']) / 100
        discount = int(request.data['discount']) / 100
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        middle_name = request.data['middle_name']

        # set the customer id to global
        global customer_id

        # get the purchase brand with the branch id
        warehouse = Warehouse.objects.get(id=warehouse_id)

        # get or create a user that made the purchase if they dont exist
        customer, created = Customer.objects.get_or_create(first_name=request.data['first_name'], last_name=request.data['last_name'], phone_number=request.data['phone_number'], defaults={
                                                           'email': request.data['email'], 'middle_name': middle_name, 'customer_type': 'wholesale'})

        # grab the id from existing or new customer
        if created:
            newly_created_customer = Customer.objects.get(
                first_name=first_name, last_name=last_name, phone_number=request.data['phone_number'])
            customer_id = str(newly_created_customer.id)
        else:
            customer_id = str(customer.id)

        # set customer to buyer to create a retail sale
        buyer = Customer.objects.get(id=customer_id)

        # save new retail sale
        wholesale = Wholesale(warehouse=warehouse, customer=buyer,
                        tax=tax, discount=discount)
        wholesale.save()

        # add spare parts and vehicles to the sale
        for vehicle in vehicles_purchased:
            wholesale.vehicles_sold.add(vehicle)

        for part in spare_parts_purchased:
            wholesale.spare_parts_sold.add(part)

        # get the list of vehicles that exist
        vehicles_in_warehouse = warehouse.vehicles_in_stock.values()
        spare_parts_in_warehouse = warehouse.spare_parts_in_stock.values()

        # list of all vehicles and spare parts yet to be received
        vehicles_in_stock = []
        spare_parts_in_stock = []

        # perform a simple check to remove every vehicle and spare part that are lined up to be received
        for vehicle in vehicles_in_warehouse:
            if str(vehicle['id']) not in vehicles_purchased:
                vehicles_in_stock.append(str(vehicle['id']))

        for part in spare_parts_in_warehouse:
            if str(part['id']) not in spare_parts_purchased:
                spare_parts_in_stock.append(str(part['id']))

        # sale remaining vehicle and spare parts to the shop
        warehouse.vehicles_in_stock.set(vehicles_in_stock)
        warehouse.spare_parts_in_stock.set(spare_parts_in_stock)
        warehouse.save()

        # serialize the branch as response
        warehouse_serializer = WarehouseDetailSerializer(
            warehouse, many=False)

        #update all the vehicles with the latest status
        Vehicle.objects.filter(id__in=vehicles_purchased).update(
            current_location="retail", custodian=f"{first_name} {middle_name} {last_name}")

        #update all the vehicles with the latest status
        SparePart.objects.filter(id__in=spare_parts_purchased).update(
            current_location="retail", custodian=f"{first_name} {middle_name} {last_name}")

        return Response(warehouse_serializer.data, status=status.HTTP_201_CREATED)





class FinanceSaleListView(ListAPIView):
    queryset = FinanceAndCorporateSale.objects.filter(sale_type="finance sale")
    serializer_class = FinanceAndCorporateSaleSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
   



class CorporateSaleListView(ListAPIView):
    queryset = FinanceAndCorporateSale.objects.filter(sale_type="corporate sale")
    serializer_class = FinanceAndCorporateSaleSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    

class FinanceAndCorporateSaleDetailView(RetrieveAPIView):
    queryset = FinanceAndCorporateSale.objects.all()
    serializer_class = FinanceAndCorporateSaleSerializer
    lookup_field = "slug"
    
