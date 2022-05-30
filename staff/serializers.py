from rest_framework import serializers
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    fullname = serializers.ReadOnlyField()

    class Meta:
        model = Staff
        fields = ("__all__")
