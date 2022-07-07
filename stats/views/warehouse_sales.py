from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from sales.models import Wholesale
from sales.serializer import WholesaleSerializer
from units.models import Warehouse

import datetime

from vehicles.models import SparePart, Vehicle


class WarehouseSalesStats(APIView):

    def get(self, request):
        specific_warehouse_slug = request.GET.get('slug')
        model = request.GET.get('model')
        brand = request.GET.get('brand')
        user_role = request.user.role
        user_workplace = request.user.workplace
        global warehouse 
        serializer = ""
        
              
        if user_role == "Super Admin" or user_role == "Admin":
            warehouse = Warehouse.objects.get(slug=specific_warehouse_slug)


        if user_role == "Warehouse Officer":
            warehouse = Warehouse.objects.get(name=user_workplace)
        
        wholesale_query = Wholesale.objects.prefetch_related('spare_parts_sold', 'vehicles_sold' ).filter(warehouse=warehouse)
        
        
        today = datetime.datetime.now()
        current_year = today.strftime("%Y")
        current_week = today.strftime("%V")
        current_month = today.strftime("%m")
        yesterday = today - datetime.timedelta(days=1)
        
             
               
        # day's stats 
        daily_data = wholesale_query.filter(sold_at__year=current_year).filter(sold_at__week=current_week).filter(sold_at__gt=yesterday).values('vehicles_sold', 'spare_parts_sold')

        
        day_vehicles_sold = 0
        day_spare_parts_sold = 0

        
        if len(brand) == 0 and len(model) == 0:
            for x in daily_data:
                if x['vehicles_sold']:
                    day_vehicles_sold += 1
                if x['spare_parts_sold']:
                    day_spare_parts_sold += 1
        
                    

        if len(brand) > 0 and len(model) == 0:

            vehicle_ids = []
            spare_part_ids = []

            for x in daily_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))

            day_vehicles_sold = Vehicle.objects.filter(id__in=vehicle_ids, model__brand__name=brand).count()
            day_spare_parts_sold = SparePart.objects.filter(id__in=spare_part_ids, part_type__model__brand__name=brand).count()
                    
          

        if len(brand) > 0 and len(model) > 0:
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
        weekly_data = wholesale_query.filter(sold_at__year=current_year).filter(sold_at__week=current_week).values('vehicles_sold', 'spare_parts_sold')
        
        week_vehicles_sold = 0
        week_spare_parts_sold = 0

        
        if len(brand) == 0 and len(model) == 0:
            for x in weekly_data:
                if x['vehicles_sold']:
                    week_vehicles_sold += 1
                if x['spare_parts_sold']:
                    week_spare_parts_sold += 1

        if len(brand) > 0 and len(model) == 0:

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

        if len(brand) > 0 and len(model) > 0:
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
        monthly_data = wholesale_query.filter(sold_at__year=current_year).filter(sold_at__month=current_month).values('vehicles_sold', 'spare_parts_sold')
        month_vehicles_sold = 0
        month_spare_parts_sold = 0


       
        if len(brand) == 0 and len(model) == 0:
            for x in monthly_data:
                if x['vehicles_sold']:
                    month_vehicles_sold += 1
                if x['spare_parts_sold']:
                    month_spare_parts_sold += 1


        if len(brand) > 0 and len(model) == 0:
           
            vehicle_ids = []
            spare_part_ids = []
            
            for x in monthly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))
                    
            month_vehicles_sold = Vehicle.objects.filter(id__in=vehicle_ids, model__brand__name = brand).count()
            month_spare_parts_sold = SparePart.objects.filter(id__in=spare_part_ids, part_type__model__brand__name = brand).count()
         
                       
        if len(brand) > 0 and len(model) > 0:
            vehicle_ids = []
            spare_part_ids = []
            
            for x in monthly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))
                    
            month_vehicles_sold = Vehicle.objects.filter(id__in=vehicle_ids, model__brand__name = brand, model__name=model).count()
            month_spare_parts_sold = SparePart.objects.filter(id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()
                       
       
        
        
        # year's stats 
      
        yearly_data = wholesale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year).values('vehicles_sold', 'spare_parts_sold')
        year_vehicles_sold = 0
        year_spare_parts_sold = 0


       
        if len(brand) == 0 and len(model) == 0:
            for x in yearly_data:
                if x['vehicles_sold']:
                    year_vehicles_sold += 1
                if x['spare_parts_sold']:
                    year_spare_parts_sold += 1


        if len(brand) > 0 and len(model) == 0:
           
            vehicle_ids = []
            spare_part_ids = []
            
            for x in yearly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))
                    
            year_vehicles_sold = Vehicle.objects.filter(id__in=vehicle_ids, model__brand__name = brand).count()
            year_spare_parts_sold = SparePart.objects.filter(id__in=spare_part_ids, part_type__model__brand__name = brand).count()
         
                       
        if len(brand) > 0 and len(model) > 0:
            vehicle_ids = []
            spare_part_ids = []
            
            for x in yearly_data:
                if x['vehicles_sold']:
                    vehicle_ids.append(str(x['vehicles_sold']))
                if x['spare_parts_sold']:
                    spare_part_ids.append(str(x['spare_parts_sold']))
                    
            year_vehicles_sold = Vehicle.objects.filter(id__in=vehicle_ids, model__brand__name = brand, model__name=model).count()            
            year_spare_parts_sold = SparePart.objects.filter(id__in=spare_part_ids, part_type__model__brand__name=brand, part_type__model__name=model).count()
            
                       
        
        # sales per month this year
        months_sales = []
        
        sales_for_the_year = wholesale_query.prefetch_related('spare_parts_sold', 'vehicles_sold').filter(sold_at__year=current_year)
        # print(sales_for_the_year.values("spare_parts_sold__part_type__model__name"))
        months = sales_for_the_year.datetimes("sold_at", kind="month")
        
            
        if len(brand) == 0 and len(model) == 0:
            for month in months:
                month_sales = sales_for_the_year.filter(sold_at__month=month.month)
                spare_parts_month_total = month_sales.aggregate(total=Count("spare_parts_sold")).get("total")
                vehicles_month_total = month_sales.aggregate(total=Count("vehicles_sold")).get("total")
                
                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })
                    
            # print(f"Month: {month.strftime('%B')}, Spare Parts Total: {spare_parts_month_total}, Vehicles Total: {vehicles_month_total}")
        
        
        if len(brand) > 0 and len(model) == 0:
            for month in months:
                month_sales = sales_for_the_year.filter(sold_at__month=month.month)
                # print(month_sales.values("spare_parts_sold__part_type__model__name"))
                spare_parts_month_total = month_sales.filter(spare_parts_sold__part_type__model__brand__name=brand).aggregate(total=Count("spare_parts_sold")).get("total")
                vehicles_month_total = month_sales.filter(vehicles_sold__model__brand__name=brand).aggregate(
                    total=Count("vehicles_sold")).get("total")
                
                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })
                    
            # print(f"Month: {month.strftime('%B')}, Spare Parts Total: {spare_parts_month_total}, Vehicles Total: {vehicles_month_total}")
        
    
        if len(brand) > 0 and len(model) > 0:
            for month in months:
                month_sales = sales_for_the_year.filter(sold_at__month=month.month)
                spare_parts_month_total = month_sales.filter(spare_parts_sold__part_type__model__brand__name=brand, spare_parts_sold__part_type__model__name=model).aggregate(
                    total=Count("spare_parts_sold")).get("total")
                vehicles_month_total = month_sales.filter(vehicles_sold__model__brand__name=brand, vehicles_sold__model__name=model).aggregate(
                    total=Count("vehicles_sold")).get("total")
                
                months_sales.append({
                    "month": month.strftime('%B'),
                    "spare_parts_total": spare_parts_month_total,
                    "vehicles_total": vehicles_month_total
                })
                    
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





class WarehouseSalesTrend(APIView):
    
    def get(self, request):
        
        specific_warehouse_slug = request.GET.get('slug')
        user_role = request.user.role
        user_workplace = request.user.workplace
        global warehouse 
        
              
        if user_role == "Super Admin" or user_role == "Admin":
            warehouse = Warehouse.objects.get(slug=specific_warehouse_slug)


        if user_role == "Warehouse Officer":
            warehouse = Warehouse.objects.get(name=user_workplace)
        
                
        all_time_sales = Wholesale.prefetch_related('spare_parts_sold', 'vehicles_sold').objects.filter(warehouse=warehouse)
        years = all_time_sales.datetimes("sold_at", kind="year")
        
    
        years_sales = []

        for year in years:
            year_sales = all_time_sales.filter(sold_at__year=year.year)
            spare_parts_year_total = year_sales.aggregate(total=Count("spare_parts_sold")).get("total")
            vehicles_year_total = year_sales.aggregate(total=Count("vehicles_sold")).get("total")

            years_sales.append({
                "year": year.strftime('%Y'),
                "spare_parts_total": spare_parts_year_total,
                "vehicles_total": vehicles_year_total
            })

            # print(f"Month: {year.strftime('%Y')}, Spare Parts Total: {spare_parts_year_total}, Vehicles Total: {vehicles_year_total}")


            context = {
                "sales_by_year": years_sales
            }
            
        return Response(context)
