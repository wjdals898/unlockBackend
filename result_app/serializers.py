from .models import *
from rest_framework import serializers

class ResultSerializer(serializers.ModelSerializer):
    #prescription_id = PrescriptionSerializer(many=True, read_only=True)
    class Meta:
        model = Result
        fields = [
            'counselor',
            'counselee',
            'date',
            'video_url',
            'analysis_url',
            'prescription_id'
        ]

class PrescriptionSerializer(serializers.ModelSerializer):
    result = ResultSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"




