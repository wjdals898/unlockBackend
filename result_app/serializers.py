from .models import *
from rest_framework import serializers


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = "__all__"

class ResultSerializer(serializers.ModelSerializer):
    prescription_id = PrescriptionSerializer(many=True, read_only=True)
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



