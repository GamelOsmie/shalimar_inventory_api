from .views import StaffListView, StaffDetailView, StaffFullListView
from django.urls import path


urlpatterns = [
    path('staff/', StaffListView.as_view(), name="Employees"),
    path('staff/full-list/', StaffFullListView.as_view(), name="All Employees"),
    path('staff/<slug>/', StaffDetailView.as_view(), name="Employees"),
    # path('export/staff/', ExportStaffInExcel.as_view(), name="Export Staff"),
]