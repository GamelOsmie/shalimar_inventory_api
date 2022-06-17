from .views import  AddSparePartsToContainerView, AddVehiclesToContainerView, BranchSparePartsSupplyDetailView, BranchSparePartsSupplyListView, BranchSparePartsSupplyReceiveView, BranchVehiclesSupplyDetailView, BranchVehiclesSupplyListView, BranchVehiclesSupplyReceiveView, CommercialInvoiceListView, ContainerListCreateView, ProformaInvoiceListView, ShipmentListView,  ShipmentDetailView, ContainerDetailView, UnlinkedCommercialInvoiceListView, UnlinkedProformaInvoiceListView, UpdateBranchDamagedSpareParts, UpdateBranchDamagedVehicles, UpdateBranchMissingSpareParts, UpdateBranchMissingVehicles, UpdateWarehouseDamagedSpareParts, UpdateWarehouseDamagedVehicles, UpdateWarehouseMissingSpareParts, UpdateWarehouseMissingVehicles, WarehouseSparePartsSupplyDetailView, WarehouseSparePartsSupplyListView, WarehouseSparePartsSupplyReceiveView, WarehouseVehiclesSupplyDetailView, WarehouseVehiclesSupplyListView, WarehouseVehiclesSupplyReceiveView
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
    path('supply/spare-parts/warehouse/', WarehouseSparePartsSupplyListView.as_view(), name="Warehouse-SpareParts-Supplies"),
    path('supply/spare-parts/warehouse/<slug>/', WarehouseSparePartsSupplyDetailView.as_view(), name="Warehouse-SpareParts-Supply"),
    
    path('supply/vehicles/branch/', BranchVehiclesSupplyListView.as_view(), name="Branch-Vehicles-Supplies"),
    path('supply/vehicles/branch/<slug>/', BranchVehiclesSupplyDetailView.as_view(), name="Branch-Vehicles-Supply"),
    path('supply/spare-parts/branch/', BranchSparePartsSupplyListView.as_view(), name="Branch-SpareParts-Supplies"),
    path('supply/spare-parts/branch/<slug>/', BranchSparePartsSupplyDetailView.as_view(), name="Branch-SpareParts-Supply"),
    
    path('receive/warehouse/vehicles/', WarehouseVehiclesSupplyReceiveView.as_view(), name="Warehouse-Vehicles-Receive"),
    path('receive/warehouse/spare-parts/', WarehouseSparePartsSupplyReceiveView.as_view(), name="Warehouse-SpareParts-Receive"),
    
    path('receive/branch/vehicles/', BranchVehiclesSupplyReceiveView.as_view(), name="Branch-Vehicles-Receive"),
    path('receive/branch/spare-parts/', BranchSparePartsSupplyReceiveView.as_view(), name="Branch-SpareParts-Receive"),

    path('supply/vehicles/branch/', BranchVehiclesSupplyListView.as_view(), name="Branch-Vehicles-Supplies"),
    path('supply/vehicles/branch/<slug>/', BranchVehiclesSupplyDetailView.as_view(), name="Branch-Vehicles-Supply"),

    path('supply/spare_parts/branch/', BranchSparePartsSupplyListView.as_view(), name="Branch-Spare-Parts-Supplies"),
    path('supply/spare_parts/branch/<slug>/', BranchSparePartsSupplyDetailView.as_view(), name="Branch-Spare-Parts-Supply"),
    
    path('warehouse/update/missing-vehicles/', UpdateWarehouseMissingVehicles.as_view(), name="Warehouse-Missing-Vehicles"),
    path('warehouse/update/damaged-vehicles/', UpdateWarehouseDamagedVehicles.as_view(), name="Warehouse-Damaged-Vehicles"),
    
    path('warehouse/update/missing-spare-parts/', UpdateWarehouseMissingSpareParts.as_view(), name="Warehouse-Missing-SpareParts"),
    path('warehouse/update/damaged-spare-parts/', UpdateWarehouseDamagedSpareParts.as_view(), name="Warehouse-Damaged-SpareParts"),
    
    path('branch/update/missing-vehicles/', UpdateBranchMissingVehicles.as_view(), name="Branch-Missing-Vehicles"),
    path('branch/update/damaged-vehicles/', UpdateBranchDamagedVehicles.as_view(), name="Branch-Damaged-Vehicles"),
    
    path('branch/update/missing-spare-parts/', UpdateBranchMissingSpareParts.as_view(), name="Branch-Missing-SpareParts"),
    path('branch/update/damaged-spare-parts/', UpdateBranchDamagedSpareParts.as_view(), name="Branch-Damaged-SpareParts"),
]
