from .views import UserList, UserDetails
from django.urls import path


urlpatterns = [
    path('users/', UserList.as_view(), name="Users"),
    path('users/<slug>/', UserDetails.as_view(), name="Users"),
]
