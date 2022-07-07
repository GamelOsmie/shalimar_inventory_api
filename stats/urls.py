from django.urls import path

from stats.views.admin import AdminCustomersSummary, AdminDashboardSummary, AdminSalesSummary
from stats.views.tracking_officer import ShipmentDashboard
from stats.views.warehouse_sales import WarehouseSalesStats, WarehouseSalesTrend
from stats.views.branch_sales import BranchSalesStats, BranchSalesTrend



urlpatterns = [
    path('stats/admin/dashboard/', AdminDashboardSummary.as_view(), name="Dashboard"),
    path('stats/shipment/dashboard/', ShipmentDashboard.as_view(), name="shipment stats"),
    
    path('stats/admin/customers-summary/', AdminCustomersSummary.as_view(), name="shipment stats"),
        
    path('stats/admin/sales/', AdminSalesSummary.as_view(), name="admin sales"),
    path('stats/branch/sales/', BranchSalesStats.as_view(), name="branch sales"),
    path('stats/branch/sales-trend/', BranchSalesTrend.as_view(), name="branch sales trends"),
    
    path('stats/warehouse/sales/', WarehouseSalesStats.as_view(), name="warehouse sales"),
    path('stats/warehouse/sales-trend/', WarehouseSalesTrend.as_view(), name="warehouse sales trends"),
]
