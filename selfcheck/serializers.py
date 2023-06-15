from .models import *
from accounts.serializers import CounseleeSerializer
from rest_framework import serializers


class SelfCheckSerializer(serializers.ModelSerializer):
    counselee_id = CounseleeSerializer(read_only=True)
    #user = counselee_id.data

    class Meta:
        model = SelfCheck
        fields = '__all__'
