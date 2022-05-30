from .views import  CommercialInvoiceListView, ProformaInvoiceListView, ShipmentListView, ContainerCreateView, ShipmentDetailView, ContainerListView, ContainerDetailView, WarehouseSupplyDetailView, WarehouseSupplyListView, WarehouseSupplyReceiveView
from django.urls import path


urlpatterns = [
    path('invoices/commercial/', CommercialInvoiceListView.as_view(), name="Commercial-Invoices"),
    path('invoices/proforma/', ProformaInvoiceListView.as_view(), name="Proforma-Invoices"),
    
    path('shipments/', ShipmentListView.as_view(), name="Shipments"),
    path('shipments/<slug>/', ShipmentDetailView.as_view(), name="Shipment"),
    
    path('containers/', ContainerListView.as_view(), name="Containers"),
    path('containers/add/', ContainerCreateView.as_view(), name="Container-Creation"),
    path('containers/<slug>/', ContainerDetailView.as_view(), name="Container"),
    
    path('supply/warehouse/', WarehouseSupplyListView.as_view(), name="Warehouse Supplies"),
    path('supply/warehouse/<slug>/', WarehouseSupplyDetailView.as_view(), name="Warehouse Operation"),
    path('supply/warehouse/receive/', WarehouseSupplyReceiveView.as_view(), name="Warehouse Operation"),
]
