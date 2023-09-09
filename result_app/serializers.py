from .models import *
from rest_framework import serializers


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = [
            'id',
            'counselor',
            'counselee',
            'date',
            'analysis_url',
            'video',
        ]


class PrescriptionSerializer(serializers.ModelSerializer):
    result = ResultSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"

