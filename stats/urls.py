from django.urls import path

from stats.views.admin import DashboardSummary
from stats.views.tracking_officer import ShipmentDashboard



urlpatterns = [
    path('stats/admin/dashboard/', DashboardSummary.as_view(), name="Dashboard"),
    path('stats/shipment/dashboard/', ShipmentDashboard.as_view(), name="Dashboard"),
]
