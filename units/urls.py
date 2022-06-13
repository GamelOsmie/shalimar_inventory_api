from .views import BranchListView, BranchDetailsView, ServiceShopDetailsView, ServiceShopListView, WarehouseListView, WarehouseDetailsView, WarehouseRetrieveView
from django.urls import path


urlpatterns = [
    path('branches/', BranchListView.as_view(), name="Branches"),
    path('branches/<slug>/', BranchDetailsView.as_view(), name="Branch"),

    path('warehouses/', WarehouseListView.as_view(), name="Warehouses"),
    path('warehouses/get/', WarehouseRetrieveView.as_view(), name="Get-Warehouse"),
    path('warehouses/<slug>/', WarehouseDetailsView.as_view(), name="Warehouse"),

    path('service-shops/', ServiceShopListView.as_view(), name="Service Shops"),
    path('service-shops/<slug>/', ServiceShopDetailsView.as_view(), name="Service Shop"),
]
