from .views import BrandListView, ModelListView, ModelDetailView, TaxDetailView, TaxListView, VehicleListView, SparePartListView,  SparePartDetailView, SparePartTypeListView,  SparePartTypeDetailView
from django.urls import path


urlpatterns = [
    path('tax/', TaxListView.as_view(), name="taxes"),
    path('tax/<id>', TaxDetailView.as_view(), name="tax"),
    path('brands/', BrandListView.as_view(), name="Brands"),
    path('models/', ModelListView.as_view(), name="Models"),
    path('models/<slug>/', ModelDetailView.as_view(), name="Model"),
    path('vehicles/', VehicleListView.as_view(), name="Vehicles"),
    path('spare-parts/', SparePartListView.as_view(), name="Spare Parts"),
    path('spare-parts/<slug>/', SparePartDetailView.as_view(), name="Spare Part"),
    path('spare-parts-type/', SparePartTypeListView.as_view(), name="Spare Part Types"),
    path('spare-parts-type/<slug>/', SparePartTypeDetailView.as_view(), name="Spare Part Type"),
]
