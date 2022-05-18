from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .models import Brand, Model, SparePart, SparePartType, Tax, Vehicle
from .serializers import BrandSerializer, SparePartSerializer,  SparePartTypeSerializer, TaxSerializer, VehicleModelSerializer, VehicleSerializer
from rest_framework.filters import SearchFilter



class TaxListView(ListCreateAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class TaxDetailView(UpdateAPIView):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
    lookup_field = "id"


class BrandListView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ModelListView(ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = VehicleModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ('brand__name', 'name')
    
    def perform_create(self, serializer):
        return serializer.save(tax=1)


class ModelDetailView(RetrieveUpdateAPIView):
    queryset = Model.objects.all()
    serializer_class = VehicleModelSerializer
    lookup_field = "slug"


class VehicleListView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    filter_backends = [SearchFilter]
    search_fields = ['engine_number', 'chassis_number']


class SparePartTypeListView(ListCreateAPIView):
    queryset = SparePartType.objects.all()
    serializer_class = SparePartTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['model__name', 'model__brand__name' ,'part']
    
    def perform_create(self, serializer):
        return serializer.save(tax=1)


class SparePartTypeDetailView(RetrieveUpdateAPIView):
    queryset = SparePartType.objects.all()
    serializer_class = SparePartTypeSerializer
    lookup_field = "slug"


class SparePartListView(ListCreateAPIView):
    queryset = SparePart.objects.all()
    serializer_class = SparePartSerializer
    filter_backends = [SearchFilter]
    search_fields = ['part_number', 'part_type__part', ]


class SparePartDetailView(RetrieveUpdateAPIView):
    queryset = SparePart.objects.all()
    serializer_class = SparePartSerializer
    lookup_field = "slug"
