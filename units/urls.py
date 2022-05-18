from .views import BranchListView, BranchDetailsView, WarehouseListView, WarehouseDetailsView
from django.urls import path


urlpatterns = [
    path('branches/', BranchListView.as_view(), name="Branches"),
    path('branches/<slug>/', BranchDetailsView.as_view(), name="Branch"),

    path('warehouses/', WarehouseListView.as_view(), name="Warehouses"),
    path('warehouses/<slug>/', WarehouseDetailsView.as_view(), name="Warehouse"),

    path('service-shops/', WarehouseListView.as_view(), name="Service Shops"),
    path('service-shops/<slug>/', WarehouseDetailsView.as_view(), name="Service Shop"),
]
