import datetime
from multiprocessing import context
from inflection import ordinal
from rest_framework.views import APIView
from rest_framework.response import Response
from operations.models import Container, Shipment
from sales.models import Customer, FinanceAndCorporateSale, Organization, Retail, Wholesale
from django.db.models import Sum, Count
from staff.models import Staff
from units.models import Branch, ServiceShop, Warehouse
from users.models import User
from vehicles.models import Brand, Model, SparePart, SparePartType, Vehicle


class AdminDashboardSummary(APIView):

    def get(self, request):
        external_locations = ['finance sale', 'corporate sale',
                              'wholesale', 'retail', 'damaged', 'missing']

        staff = Staff.objects.all().count()
        users = User.objects.all().exclude(role="Super Admin").count()
        warehouses = Warehouse.objects.all().count()
        branches = Branch.objects.all().count()
        service_shops = ServiceShop.objects.all().count()
        spare_parts = SparePart.objects.exclude(
            current_location__in=external_locations).count()
        vehicles = Vehicle.objects.exclude(
            current_location__in=external_locations).count()
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


class AdminCustomersSummary(APIView):

    def get(self, request):

        individuals = Customer.objects.all()
        business = Organization.objects.all()

        retail_customers = individuals.filter(customer_type="retail").count()
        wholesale_customers = individuals.filter(
            customer_type="wholesale").count()
        finance_sale_customers = business.filter(
            consumption_type="finance sale").count()
        corporate_sale_customers = business.filter(
            consumption_type="corporate sale").count()

        context = {
            "retail_customers": retail_customers,
            "wholesale_customers": wholesale_customers,
            "finance_sale_customers": finance_sale_customers,
            "corporate_sale_customers": corporate_sale_customers
        }

        return Response(context)


class AdminSalesSummary(APIView):

    def get(self, request):
        model = request.GET.get('model')
        brand = request.GET.get('brand')
        sale_type = request.GET.get('sale_type')

        retail_query = Retail.objects.prefetch_related(
            'spare_parts_sold', 'vehicles_sold').all()
        wholesale_query = Wholesale.objects.prefetch_related(
            'spare_parts_sold', 'vehicles_sold').all()
        business_sale_query = FinanceAndCorporateSale.objects.prefetch_related(
            'spare_parts_sold', 'vehicles_sold').all()

        today = datetime.datetime.now()
        current_year = today.strftime("%Y")
        current_week = today.strftime("%V")
        current_month = today.strftime("%m")
        yesterday = today - datetime.timedelta(days=1)

        # day's stats
        daily_retail_data = []
        daily_wholesale_data = []
        daily_corporate_sale_data = []
        daily_finance_sale_data = []

        daily_data = []

        daily_retail_data = retail_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year).filter(
            sold_at__week=current_week).filter(sold_at__gt=yesterday).values('vehicles_sold', 'spare_parts_sold')
        daily_wholesale_data = wholesale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year).filter(
            sold_at__week=current_week).filter(sold_at__gt=yesterday).values('vehicles_sold', 'spare_parts_sold')
        daily_corporate_sale_data = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year).filter(
            sold_at__week=current_week).filter(sold_at__gt=yesterday).filter(sale_type="corporate sale").values('vehicles_sold', 'spare_parts_sold')
        daily_finance_sale_data = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year).filter(
            sold_at__week=current_week).filter(sold_at__gt=yesterday).filter(sale_type="finance sale").values('vehicles_sold', 'spare_parts_sold')

        if len(sale_type) > 0:
            if (sale_type == "retail"):
                daily_data = daily_retail_data

            if (sale_type == "wholesale"):
                daily_data = daily_wholesale_data

            if (sale_type == "finance_sale"):
                daily_data = daily_finance_sale_data

            if (sale_type == "corporate_sale"):
                daily_data = daily_corporate_sale_data

        day_vehicles_sold = 0
        day_spare_parts_sold = 0

        # no query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) == 0:
            for x in daily_retail_data:
                if x['vehicles_sold']:
                    day_vehicles_sold += 1
                if x['spare_parts_sold']:
                    day_spare_parts_sold += 1

            for x in daily_wholesale_data:
                if x['vehicles_sold']:
                    day_vehicles_sold += 1
                if x['spare_parts_sold']:
                    day_spare_parts_sold += 1

            for x in daily_corporate_sale_data:
                if x['vehicles_sold']:
                    day_vehicles_sold += 1
                if x['spare_parts_sold']:
                    day_spare_parts_sold += 1

            for x in daily_finance_sale_data:
                if x['vehicles_sold']:
                    day_vehicles_sold += 1
                if x['spare_parts_sold']:
                    day_spare_parts_sold += 1

        # sale type query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) > 0:
            for x in daily_data:
                if x['vehicles_sold']:
                    day_vehicles_sold += 1
                if x['spare_parts_sold']:
                    day_spare_parts_sold += 1
                    

        # brand set and no other query param set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in daily_retail_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in daily_wholesale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in daily_finance_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in daily_corporate_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            day_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand).count()
            day_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand).count()

        # brand set and model is set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in daily_retail_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in daily_wholesale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in daily_finance_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in daily_corporate_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            day_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand, model__name=model).count()
            day_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()
            

        # brand set and sale type set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) > 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in daily_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            day_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand).count()
            day_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand).count()

        # brand, models set and sale type set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) > 0:
            vehicle_ids = []
            spare_part_ids = []

            for x in daily_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            day_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand, model__name=model).count()
            day_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()
            
            

        # week's stats
        weekly_retail_data = []
        weekly_wholesale_data = []
        weekly_corporate_sale_data = []
        weekly_finance_sale_data = []

        weekly_data = []

        weekly_retail_data = retail_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sold_at__week=current_week).values('vehicles_sold', 'spare_parts_sold')
        weekly_wholesale_data = wholesale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year).filter(
            sold_at__week=current_week).values('vehicles_sold', 'spare_parts_sold')
        weekly_corporate_sale_data = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sold_at__week=current_week).filter(sale_type="corporate sale").values('vehicles_sold', 'spare_parts_sold')
        weekly_finance_sale_data = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sold_at__week=current_week).filter(sale_type="finance sale").values('vehicles_sold', 'spare_parts_sold')


        if len(sale_type) > 0:
            if (sale_type == "retail"):
                weekly_data = weekly_retail_data

            if (sale_type == "wholesale"):
                weekly_data = weekly_wholesale_data

            if (sale_type == "finance_sale"):
                weekly_data = weekly_finance_sale_data

            if (sale_type == "corporate_sale"):
                weekly_data = weekly_corporate_sale_data
                

        week_vehicles_sold = 0
        week_spare_parts_sold = 0
        

     # no query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) == 0:
            for x in weekly_retail_data:
                if x['vehicles_sold']:
                    week_vehicles_sold += 1
                if x['spare_parts_sold']:
                    week_spare_parts_sold += 1

            for x in weekly_wholesale_data:
                if x['vehicles_sold']:
                    week_vehicles_sold += 1
                if x['spare_parts_sold']:
                    week_spare_parts_sold += 1

            for x in weekly_corporate_sale_data:
                if x['vehicles_sold']:
                    week_vehicles_sold += 1
                if x['spare_parts_sold']:
                    week_spare_parts_sold += 1

            for x in weekly_finance_sale_data:
                if x['vehicles_sold']:
                    week_vehicles_sold += 1
                if x['spare_parts_sold']:
                    week_spare_parts_sold += 1
                    
                    
                    
        # sale type query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) > 0:
            for x in weekly_data:
                if x['vehicles_sold']:
                    week_vehicles_sold += 1
                if x['spare_parts_sold']:
                    week_spare_parts_sold += 1
  
                    

        # brand set and no other query param set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in weekly_retail_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in weekly_wholesale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in weekly_finance_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in weekly_corporate_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            week_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand).count()
            week_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand).count()
            
            
        # brand set and model is set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in weekly_retail_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in weekly_wholesale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in weekly_finance_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in weekly_corporate_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            week_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand, model__name=model).count()
            week_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()
            
            
         # brand set and sale type set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) > 0:
    
            vehicle_ids = []
            spare_part_ids = []

            for x in weekly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            week_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand).count()
            week_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand).count()
            
            
          # brand, models set and sale type set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) > 0:
            vehicle_ids = []
            spare_part_ids = []

            for x in weekly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            week_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand, model__name=model).count()
            week_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()



        # month's stats
        monthly_retail_data = []
        monthly_wholesale_data = []
        monthly_corporate_sale_data = []
        monthly_finance_sale_data = []

        monthly_data = []

        monthly_retail_data = retail_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sold_at__month=current_month).values('vehicles_sold', 'spare_parts_sold')
        monthly_wholesale_data = wholesale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year).filter(
            sold_at__month=current_month).values('vehicles_sold', 'spare_parts_sold')
        monthly_corporate_sale_data = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sold_at__month=current_month).filter(sale_type="corporate sale").values('vehicles_sold', 'spare_parts_sold')
        monthly_finance_sale_data = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sold_at__month=current_month).filter(sale_type="finance sale").values('vehicles_sold', 'spare_parts_sold')

        if len(sale_type) > 0:
            if (sale_type == "retail"):
                monthly_data = monthly_retail_data

            if (sale_type == "wholesale"):
                monthly_data = monthly_wholesale_data

            if (sale_type == "finance_sale"):
                monthly_data = monthly_finance_sale_data

            if (sale_type == "corporate_sale"):
                monthly_data = monthly_corporate_sale_data

        month_vehicles_sold = 0
        month_spare_parts_sold = 0

     # no query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) == 0:
            for x in monthly_retail_data:
                if x['vehicles_sold']:
                    month_vehicles_sold += 1
                if x['spare_parts_sold']:
                    month_spare_parts_sold += 1

            for x in monthly_wholesale_data:
                if x['vehicles_sold']:
                    month_vehicles_sold += 1
                if x['spare_parts_sold']:
                    month_spare_parts_sold += 1

            for x in monthly_corporate_sale_data:
                if x['vehicles_sold']:
                    month_vehicles_sold += 1
                if x['spare_parts_sold']:
                    month_spare_parts_sold += 1

            for x in monthly_finance_sale_data:
                if x['vehicles_sold']:
                    month_vehicles_sold += 1
                if x['spare_parts_sold']:
                    month_spare_parts_sold += 1

        # sale type query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) > 0:
            for x in monthly_data:
                if x['vehicles_sold']:
                    month_vehicles_sold += 1
                if x['spare_parts_sold']:
                    month_spare_parts_sold += 1

        # brand set and no other query param set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in monthly_retail_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in monthly_wholesale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in monthly_finance_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in monthly_corporate_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            week_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand).count()
            week_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand).count()

        # brand set and model is set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in monthly_retail_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in monthly_wholesale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in monthly_finance_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in monthly_corporate_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            month_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand, model__name=model).count()
            month_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()

         # brand set and sale type set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) > 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in monthly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            month_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand).count()
            month_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand).count()

          # brand, models set and sale type set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) > 0:
            vehicle_ids = []
            spare_part_ids = []

            for x in monthly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            month_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand, model__name=model).count()
            month_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()      
        
        

        # year's stats
        yearly_retail_data = []
        yearly_wholesale_data = []
        yearly_corporate_sale_data = []
        yearly_finance_sale_data = []

        yearly_data = []

        yearly_retail_data = retail_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).values('vehicles_sold', 'spare_parts_sold')
        yearly_wholesale_data = wholesale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year).values('vehicles_sold', 'spare_parts_sold')
        yearly_corporate_sale_data = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sale_type="corporate sale").values('vehicles_sold', 'spare_parts_sold')
        yearly_finance_sale_data = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sale_type="finance sale").values('vehicles_sold', 'spare_parts_sold')

        if len(sale_type) > 0:
            if (sale_type == "retail"):
                yearly_data = yearly_retail_data

            if (sale_type == "wholesale"):
                yearly_data = yearly_wholesale_data

            if (sale_type == "finance_sale"):
                yearly_data = yearly_finance_sale_data

            if (sale_type == "corporate_sale"):
                yearly_data = yearly_corporate_sale_data

        year_vehicles_sold = 0
        year_spare_parts_sold = 0


     # no query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) == 0:
            for x in yearly_retail_data:
                if x['vehicles_sold']:
                    year_vehicles_sold += 1
                if x['spare_parts_sold']:
                    year_spare_parts_sold += 1

            for x in yearly_wholesale_data:
                if x['vehicles_sold']:
                    year_vehicles_sold += 1
                if x['spare_parts_sold']:
                    year_spare_parts_sold += 1

            for x in yearly_corporate_sale_data:
                if x['vehicles_sold']:
                    year_vehicles_sold += 1
                if x['spare_parts_sold']:
                    year_spare_parts_sold += 1

            for x in yearly_finance_sale_data:
                if x['vehicles_sold']:
                    year_vehicles_sold += 1
                if x['spare_parts_sold']:
                    year_spare_parts_sold += 1

        # sale type query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) > 0:
            for x in yearly_data:
                if x['vehicles_sold']:
                    year_vehicles_sold += 1
                if x['spare_parts_sold']:
                    year_spare_parts_sold += 1

        # brand set and no other query param set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in yearly_retail_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in yearly_wholesale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in yearly_finance_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in yearly_corporate_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            week_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand).count()
            week_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand).count()
            

        # brand set and model is set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in yearly_retail_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in yearly_wholesale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in yearly_finance_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            for x in yearly_corporate_sale_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            year_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand, model__name=model).count()
            month_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()


         # brand set and sale type set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) > 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in yearly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            year_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand).count()
            year_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand).count()

          # brand, models set and sale type set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) > 0:
            vehicle_ids = []
            spare_part_ids = []

            for x in yearly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            year_vehicles_sold = Vehicle.objects.filter(
                id__in=vehicle_ids, model__brand__name=brand, model__name=model).count()
            year_spare_parts_sold = SparePart.objects.filter(
                id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()

     
       
       
        # sales per month this year
        retail_sales_of_the_year = []
        wholesale_sales_of_the_year = []
        corporate_sale_sales_of_the_year = []
        finance_sale_sales_of_the_year = []
        
        months_sales = []

        retail_sales_of_the_year = retail_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).values('vehicles_sold', 'spare_parts_sold')
        wholesale_sales_of_the_year = wholesale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).values('vehicles_sold', 'spare_parts_sold')
        corporate_sale_sales_of_the_year = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sale_type="corporate sale").values('vehicles_sold', 'spare_parts_sold')
        finance_sale_sales_of_the_year = business_sale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(
            sold_at__year=current_year).filter(sale_type="finance sale").values('vehicles_sold', 'spare_parts_sold')
        
        
        # print(sales_for_the_year.values("spare_parts_sold__part_type__model__name"))
        
        # use of the of the sales to get the number of months
        months = retail_sales_of_the_year.datetimes("sold_at", kind="month")
        
        
        # no query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) == 0:
            for month in months:
                
                retail_sales = retail_sales_of_the_year.filter(sold_at__month=month.month)
                retail_spare_parts_month_total = retail_sales.aggregate(total=Count("spare_parts_sold")).get("total")
                retail_vehicles_month_total = retail_sales.aggregate(total=Count("vehicles_sold")).get("total")
                
                
                wholesale_sales = wholesale_sales_of_the_year.filter(sold_at__month=month.month)
                wholesale_spare_parts_month_total = wholesale_sales.aggregate(
                    total=Count("spare_parts_sold")).get("total")
                wholesale_vehicles_month_total = wholesale_sales.aggregate(
                    total=Count("vehicles_sold")).get("total")

                
                corporate_sale_sales = corporate_sale_sales_of_the_year.filter(sold_at__month=month.month)
                corporate_sale_spare_parts_month_total = corporate_sale_sales.aggregate(
                    total=Count("spare_parts_sold")).get("total")
                corporate_sale_vehicles_month_total = corporate_sale_sales.aggregate(
                    total=Count("vehicles_sold")).get("total")

                
                finance_sale_sales = finance_sale_sales_of_the_year.filter(sold_at__month=month.month)
                finance_sale_spare_parts_month_total = finance_sale_sales.aggregate(
                    total=Count("spare_parts_sold")).get("total")
                finance_sale_vehicles_month_total = finance_sale_sales.aggregate(
                    total=Count("vehicles_sold")).get("total")

                spare_parts_month_total = (retail_spare_parts_month_total + wholesale_spare_parts_month_total + corporate_sale_spare_parts_month_total + finance_sale_spare_parts_month_total )

                vehicles_month_total = (retail_vehicles_month_total + wholesale_vehicles_month_total + corporate_sale_vehicles_month_total + finance_sale_vehicles_month_total )


                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })


        # sale type query params set
        if len(brand) == 0 and len(model) == 0 and len(sale_type) > 0:
                  
            for month in months:
                
                spare_parts_month_total = 0
                vehicles_month_total = 0
                      
                if (sale_type == "retail"):
                    retail_sales = retail_sales_of_the_year.filter(sold_at__month=month.month)
                    retail_spare_parts_month_total = retail_sales.aggregate(total=Count("spare_parts_sold")).get("total")
                    retail_vehicles_month_total = retail_sales.aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = retail_spare_parts_month_total
                    vehicles_month_total = retail_vehicles_month_total

                if (sale_type == "wholesale"):
                    wholesale_sales = wholesale_sales_of_the_year.filter(sold_at__month=month.month)
                    wholesale_spare_parts_month_total = wholesale_sales.aggregate(total=Count("spare_parts_sold")).get("total")
                    wholesale_vehicles_month_total = wholesale_sales.aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = wholesale_spare_parts_month_total
                    vehicles_month_total =  wholesale_vehicles_month_total


                if (sale_type == "corporate_sale"):
                    corporate_sale_sales = corporate_sale_sales_of_the_year.filter(sold_at__month=month.month)
                    corporate_sale_spare_parts_month_total = corporate_sale_sales.aggregate(total=Count("spare_parts_sold")).get("total")
                    corporate_sale_vehicles_month_total = corporate_sale_sales.aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = corporate_sale_spare_parts_month_total 
                    vehicles_month_total = corporate_sale_vehicles_month_total 

                if (sale_type == "finance_sale"):
                    finance_sale_sales = finance_sale_sales_of_the_year.filter(sold_at__month=month.month)
                    finance_sale_spare_parts_month_total = finance_sale_sales.aggregate(total=Count("spare_parts_sold")).get("total")
                    finance_sale_vehicles_month_total = finance_sale_sales.aggregate(total=Count("vehicles_sold")).get("total")

                    spare_parts_month_total = finance_sale_spare_parts_month_total

                    vehicles_month_total = finance_sale_vehicles_month_total

                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })


        # brand set and no other query param set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) == 0:
            for month in months:
                
                retail_sales = retail_sales_of_the_year.filter(sold_at__month=month.month)
                retail_spare_parts_month_total = retail_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(total=Count("spare_parts_sold")).get("total")
                retail_vehicles_month_total = retail_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(total=Count("vehicles_sold")).get("total")
                
                
                wholesale_sales = wholesale_sales_of_the_year.filter(sold_at__month=month.month)
                wholesale_spare_parts_month_total = wholesale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(total=Count("spare_parts_sold")).get("total")
                wholesale_vehicles_month_total = wholesale_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(
                    total=Count("vehicles_sold")).get("total")

                
                corporate_sale_sales = corporate_sale_sales_of_the_year.filter(sold_at__month=month.month)
                corporate_sale_spare_parts_month_total = corporate_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(
                    total=Count("spare_parts_sold")).get("total")
                corporate_sale_vehicles_month_total = corporate_sale_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(
                    total=Count("vehicles_sold")).get("total")

                
                finance_sale_sales = finance_sale_sales_of_the_year.filter(sold_at__month=month.month)
                finance_sale_spare_parts_month_total = finance_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(
                    total=Count("spare_parts_sold")).get("total")
                finance_sale_vehicles_month_total = finance_sale_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(
                    total=Count("vehicles_sold")).get("total")
                

                spare_parts_month_total = (retail_spare_parts_month_total + wholesale_spare_parts_month_total + corporate_sale_spare_parts_month_total + finance_sale_spare_parts_month_total )

                vehicles_month_total = (retail_vehicles_month_total + wholesale_vehicles_month_total + corporate_sale_vehicles_month_total + finance_sale_vehicles_month_total )


                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })
            
           # brand set and model is set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) == 0:
            for month in months:
                
                retail_sales = retail_sales_of_the_year.filter(sold_at__month=month.month)
                retail_spare_parts_month_total = retail_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("spare_parts_sold")).get("total")
                retail_vehicles_month_total = retail_sales.filter(vehicles_sold__model__brand__name=brand, vehicles_sold__model__name=model).aggregate(total=Count("vehicles_sold")).get("total")
                
                
                wholesale_sales = wholesale_sales_of_the_year.filter(sold_at__month=month.month)
                wholesale_spare_parts_month_total = wholesale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("spare_parts_sold")).get("total")
                wholesale_vehicles_month_total = wholesale_sales.filter(vehicles_sold__model__brand__name=brand, vehicles_sold__model__name=model).aggregate(
                    total=Count("vehicles_sold")).get("total")

                
                corporate_sale_sales = corporate_sale_sales_of_the_year.filter(sold_at__month=month.month)
                corporate_sale_spare_parts_month_total = corporate_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(
                    total=Count("spare_parts_sold")).get("total")
                corporate_sale_vehicles_month_total = corporate_sale_sales.filter(vehicles_sold__model__brand__name=brand, vehicles_sold__model__name=model).aggregate(
                    total=Count("vehicles_sold")).get("total")

                
                finance_sale_sales = finance_sale_sales_of_the_year.filter(sold_at__month=month.month)
                finance_sale_spare_parts_month_total = finance_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(
                    total=Count("spare_parts_sold")).get("total")
                finance_sale_vehicles_month_total = finance_sale_sales.filter(vehicles_sold__model__brand__name=brand, vehicles_sold__model__name=model).aggregate(
                    total=Count("vehicles_sold")).get("total")
                

                spare_parts_month_total = (retail_spare_parts_month_total + wholesale_spare_parts_month_total + corporate_sale_spare_parts_month_total + finance_sale_spare_parts_month_total )

                vehicles_month_total = (retail_vehicles_month_total + wholesale_vehicles_month_total + corporate_sale_vehicles_month_total + finance_sale_vehicles_month_total )


                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })
            

        # brand set and sale type set
        if len(brand) > 0 and len(model) == 0 and len(sale_type) > 0:
                  
            for month in months:
                
                spare_parts_month_total = 0
                vehicles_month_total = 0
                      
                if (sale_type == "retail"):
                    retail_sales = retail_sales_of_the_year.filter(sold_at__month=month.month)
                    retail_spare_parts_month_total = retail_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(total=Count("spare_parts_sold")).get("total")
                    retail_vehicles_month_total = retail_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = retail_spare_parts_month_total
                    vehicles_month_total = retail_vehicles_month_total

                if (sale_type == "wholesale"):
                    wholesale_sales = wholesale_sales_of_the_year.filter(sold_at__month=month.month)
                    wholesale_spare_parts_month_total = wholesale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(total=Count("spare_parts_sold")).get("total")
                    wholesale_vehicles_month_total = wholesale_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = wholesale_spare_parts_month_total
                    vehicles_month_total =  wholesale_vehicles_month_total


                if (sale_type == "corporate_sale"):
                    corporate_sale_sales = corporate_sale_sales_of_the_year.filter(sold_at__month=month.month)
                    corporate_sale_spare_parts_month_total = corporate_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(total=Count("spare_parts_sold")).get("total")
                    corporate_sale_vehicles_month_total = corporate_sale_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = corporate_sale_spare_parts_month_total 
                    vehicles_month_total = corporate_sale_vehicles_month_total 

                if (sale_type == "finance_sale"):
                    finance_sale_sales = finance_sale_sales_of_the_year.filter(sold_at__month=month.month)
                    finance_sale_spare_parts_month_total = finance_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(total=Count("spare_parts_sold")).get("total")
                    finance_sale_vehicles_month_total = finance_sale_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(total=Count("vehicles_sold")).get("total")

                    spare_parts_month_total = finance_sale_spare_parts_month_total
                    vehicles_month_total = finance_sale_vehicles_month_total

                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })


                
                
        # all query params set
        if len(brand) > 0 and len(model) > 0 and len(sale_type) > 0:
                  
            for month in months:
                
                spare_parts_month_total = 0
                vehicles_month_total = 0
                      
                if (sale_type == "retail"):
                    retail_sales = retail_sales_of_the_year.filter(sold_at__month=month.month)
                    retail_spare_parts_month_total = retail_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("spare_parts_sold")).get("total")
                    retail_vehicles_month_total = retail_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = retail_spare_parts_month_total
                    vehicles_month_total = retail_vehicles_month_total

                if (sale_type == "wholesale"):
                    wholesale_sales = wholesale_sales_of_the_year.filter(sold_at__month=month.month)
                    wholesale_spare_parts_month_total = wholesale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("spare_parts_sold")).get("total")
                    wholesale_vehicles_month_total = wholesale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = wholesale_spare_parts_month_total
                    vehicles_month_total =  wholesale_vehicles_month_total


                if (sale_type == "corporate_sale"):
                    corporate_sale_sales = corporate_sale_sales_of_the_year.filter(sold_at__month=month.month)
                    corporate_sale_spare_parts_month_total = corporate_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("spare_parts_sold")).get("total")
                    corporate_sale_vehicles_month_total = corporate_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("vehicles_sold")).get("total")
                    
                    spare_parts_month_total = corporate_sale_spare_parts_month_total 
                    vehicles_month_total = corporate_sale_vehicles_month_total 

                if (sale_type == "finance_sale"):
                    finance_sale_sales = finance_sale_sales_of_the_year.filter(sold_at__month=month.month)
                    finance_sale_spare_parts_month_total = finance_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("spare_parts_sold")).get("total")
                    finance_sale_vehicles_month_total = finance_sale_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(total=Count("vehicles_sold")).get("total")

                    spare_parts_month_total = finance_sale_spare_parts_month_total
                    vehicles_month_total = finance_sale_vehicles_month_total

                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })

                

        # if len(brand) > 0 and len(model) == 0:
        #     for month in months:
        #         month_sales = sales_for_the_year.filter(sold_at__month=month.month)
        #         # print(month_sales.values("spare_parts_sold__part_type__model__name"))
        #         spare_parts_month_total = month_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(total=Count("spare_parts_sold")).get("total")
        #         vehicles_month_total = month_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(
        #             total=Count("vehicles_sold")).get("total")

        #         months_sales.append({
        #             "month": month.strftime('%B'),
        #             "spare_parts_total": spare_parts_month_total,
        #             "vehicles_total": vehicles_month_total
        #         })

        #     # print(f"Month: {month.strftime('%B')}, Spare Parts Total: {spare_parts_month_total}, Vehicles Total: {vehicles_month_total}")

        # if len(brand) > 0 and len(model) > 0:
        #     for month in months:
        #         month_sales = sales_for_the_year.filter(sold_at__month=month.month)
        #         spare_parts_month_total = month_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(
        #             total=Count("spare_parts_sold")).get("total")
        #         vehicles_month_total = month_sales.filter(vehicles_sold__model__brand__name=brand, vehicles_sold__model__name=model).aggregate(
        #             total=Count("vehicles_sold")).get("total")

        #         months_sales.append({
        #             "month": month.strftime('%B'),
        #             "spare_parts_total": spare_parts_month_total,
        #             "vehicles_total": vehicles_month_total
        #         })

            # print(f"Month: {month.strftime('%B')}, Spare Parts Total: {spare_parts_month_total}, Vehicles Total: {vehicles_month_total}")

        context = {
            "today": {
                "vehicles_sold": day_vehicles_sold,
                "spare_parts_sold": day_spare_parts_sold,
                "total_sold": day_vehicles_sold + day_spare_parts_sold,
            },
            "week": {
                "vehicles_sold": week_vehicles_sold,
                "spare_parts_sold": week_spare_parts_sold,
                "total_sold": week_vehicles_sold + week_spare_parts_sold
            },
            "month": {
                "vehicles_sold": month_vehicles_sold,
                "spare_parts_sold": month_spare_parts_sold,
                "total_sold": month_vehicles_sold + month_spare_parts_sold
            },
            "year": {
                "vehicles_sold": year_vehicles_sold,
                "spare_parts_sold": year_spare_parts_sold,
                "total_sold": year_vehicles_sold + year_spare_parts_sold
            },
            "sales_by_months" : months_sales
        }

        return Response(context)
