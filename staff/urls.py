from .views import StaffListView, StaffDetailView
from django.urls import path


urlpatterns = [
    path('staff/', StaffListView.as_view(), name="Employees"),
    path('staff/<slug>/', StaffDetailView.as_view(), name="Employees"),
]