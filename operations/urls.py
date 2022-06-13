from .views import  AddSparePartsToContainerView, AddVehiclesToContainerView, CommercialInvoiceListView, ContainerListCreateView, ProformaInvoiceListView, ShipmentListView,  ShipmentDetailView, ContainerDetailView, UnlinkedCommercialInvoiceListView, UnlinkedProformaInvoiceListView, WarehouseSparePartsSupplyDetailView, WarehouseSparePartsSupplyListView, WarehouseSparePartsSupplyReceiveView, WarehouseVehiclesSupplyDetailView, WarehouseVehiclesSupplyListView, WarehouseVehiclesSupplyReceiveView
from django.urls import path


urlpatterns = [
    path('invoices/commercial/', CommercialInvoiceListView.as_view(), name="Commercial-Invoices"),
    path('invoices/proforma/', ProformaInvoiceListView.as_view(), name="Proforma-Invoices"),
    path('invoices/proforma/unlinked/', UnlinkedProformaInvoiceListView.as_view(), name="unlinkedProforma-Invoices"),
    path('invoices/commercial/unlinked/', UnlinkedCommercialInvoiceListView.as_view(), name="unlinkedCommercial-Invoices"),
    
    path('shipments/', ShipmentListView.as_view(), name="Shipments"),
    path('shipments/<slug>/', ShipmentDetailView.as_view(), name="Shipment"),
    
    path('containers/', ContainerListCreateView.as_view(), name="Containers"),
    path('containers/uploads/vehicles/', AddVehiclesToContainerView.as_view(), name="Add-Vehicles"),
    path('containers/uploads/spare-parts/', AddSparePartsToContainerView.as_view(), name="Add-Part"),
    path('containers/<slug>/', ContainerDetailView.as_view(), name="Container"),
    
    path('supply/vehicles/warehouse/', WarehouseVehiclesSupplyListView.as_view(), name="Warehouse-Vehicles-Supplies"),
    path('supply/vehicles/warehouse/<slug>/', WarehouseVehiclesSupplyDetailView.as_view(), name="Warehouse-Vehicles-Supply"),
    path('supply/vehicles/warehouse/receive/', WarehouseVehiclesSupplyReceiveView.as_view(), name="Warehouse-Vehicles-Receive"),
    path('supply/spare-parts/warehouse/', WarehouseSparePartsSupplyListView.as_view(), name="Warehouse-SpareParts-Supplies"),
    path('supply/spare-parts/warehouse/<slug>/', WarehouseSparePartsSupplyDetailView.as_view(), name="Warehouse-SpareParts-Supply"),
    path('supply/spare-parts/warehouse/receive/', WarehouseSparePartsSupplyReceiveView.as_view(), name="Warehouse-SpareParts-Receive"),
]
