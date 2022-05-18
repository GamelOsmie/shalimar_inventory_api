from users.serializers import UserDetailsSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from users.permissions import AdminsOnly

# Create your views here.


class CustomPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    # permission_classes = [AdminsOnly]
    # pagination_class = CustomPaginator
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name')


class UserDetails(RetrieveAPIView):
    queryset = queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    lookup_field = "slug"
