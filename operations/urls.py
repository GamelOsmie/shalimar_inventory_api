from .views import BranchOperationsDetailView, BranchOperationsListView, CommercialInvoiceListView, ProformaInvoiceListView, ServiceShopOperationsDetailView, ServiceShopOperationsListView, ShipmentListView, ContainerCreateView, ShipmentDetailView, ContainerListView, ContainerDetailView, WarehouseOperationsDetailView, WarehouseOperationsListView, WarehouseSupplyDetailView, WarehouseSupplyListView, WarehouseSupplyReceiveView
from django.urls import path


urlpatterns = [
    path('invoices/commercial/', CommercialInvoiceListView.as_view(), name="Commercial-Invoices"),
    path('invoices/proforma/', ProformaInvoiceListView.as_view(), name="Proforma-Invoices"),
    
    path('shipments/', ShipmentListView.as_view(), name="Shipments"),
    path('shipments/<slug>/', ShipmentDetailView.as_view(), name="Shipment"),
    
    path('containers/', ContainerListView.as_view(), name="Containers"),
    path('containers/add/', ContainerCreateView.as_view(), name="Container-Creation"),
    path('containers/<slug>/', ContainerDetailView.as_view(), name="Container"),
    
    path('branches/operations/', BranchOperationsListView.as_view(), name="Branch Operations"),
    path('branches/operations/<id>/', BranchOperationsDetailView.as_view(), name="Branch Operation"),    
    
    path('warehouses/operations/', WarehouseOperationsListView.as_view(), name="Warehouse Operations"),
    path('warehouses/operations/<id>/', WarehouseOperationsDetailView.as_view(), name="Warehouse Operation"),  
    
    path('service-shop/operations/', ServiceShopOperationsListView.as_view(), name="Service Shop Operations"),
    path('service-shop/operations/<id>/', ServiceShopOperationsDetailView.as_view(), name="Service Shop Operation"),  
    
    path('supply/warehouse/', WarehouseSupplyListView.as_view(), name="Warehouse Supplies"),
    path('supply/warehouse/<slug>/', WarehouseSupplyDetailView.as_view(), name="Warehouse Operation"),
    path('supply/warehouse/receive/', WarehouseSupplyReceiveView.as_view(), name="Warehouse Operation"),
]
