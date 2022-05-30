from users.serializers import UserDetailsSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from users.permissions import AdminsOnly

# Create your views here.


class CustomPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class UserList(ListAPIView):
    queryset = User.objects.all().exclude(role="Super Admin")
    serializer_class = UserDetailsSerializer
    # permission_classes = [AdminsOnly]
    # pagination_class = CustomPaginator
    filter_backends = (SearchFilter,)
    search_fields = ('first_name', 'last_name', 'middle_name', 'role', 'workplace')


class UserDetails(RetrieveUpdateDestroyAPIView):
    queryset = queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    lookup_field = "slug"

