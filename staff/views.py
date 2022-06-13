import datetime
#import xlwt
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from users.models import User
from .serializers import StaffSerializer
from .models import Staff
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class CustomPaginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StaffListView(ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    pagination_class = CustomPaginator
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('first_name', 'middle_name', 'last_name',
                     'phone_number', 'email', 'designation', 'workplace', 'role')
    filterset_fields = ['department', 'workplace', 'role', 'qualification']


class StaffFullListView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = "slug"



# class ExportStaffInExcel(APIView):

#     def get(self, request):
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename=shalimar_staff' + \
#             str(datetime.datetime.now()) + '.xls'

#         workbook = xlwt.Workbook(encoding='utf-8')
#         worksheet = workbook.add_sheet('Staff')
#         row_num = 0
#         font_style = xlwt.XFStyle()
#         font_style.font.bold = True

#         columns = ['First Name', 'Middle Name', 'Last Name', 'Phone Number', 'Email', 'Department', 'Role', 'Workplace', 'Salary', 'Qualification', 'Institution', 'DOB', 'Date Joined' ]

#         for col_num in range(len(columns)):
#             worksheet.write(row_num, col_num, str(columns[col_num]), font_style)

#         font_style = xlwt.XFStyle()

#         rows = Staff.objects.all().values_list('first_name','middle_name','last_name','phone_number', 'email', 'department', 'role', 'workplace', 'salary', 'qualification', 'institution', 'dob', 'date_joined')

#         for row in rows:
#             row_num += 1
#             for col_num in range(len(row)):
#                 worksheet.write(row_num, col_num, str(row[col_num]), font_style)

#         workbook.save(response)

#         return response
