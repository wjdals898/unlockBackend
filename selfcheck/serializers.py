from accounts.serializers import CounseleeSerializer
from .models import *
from rest_framework import serializers


class SelfCheckSerializer(serializers.ModelSerializer):
    counselee_id = CounseleeSerializer(read_only=True)

    class Meta:
        model = SelfCheck
        fields = '__all__'
