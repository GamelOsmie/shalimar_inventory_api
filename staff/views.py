from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import StaffSerializer
from .models import Staff
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter


class CustomPaginator(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000



class StaffListView(ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    pagination_class = CustomPaginator
    filter_backends = [SearchFilter]
    search_fields = ('first_name', 'middle_name', 'last_name',
                     'phone_number', 'email', 'designation', 'workplace', 'role')


class StaffDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = "slug"
