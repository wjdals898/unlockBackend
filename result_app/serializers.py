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
            #'result_csv',
        ]


class PrescriptionSerializer(serializers.ModelSerializer):
    result = ResultSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"


class CSVFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = "__all__"
