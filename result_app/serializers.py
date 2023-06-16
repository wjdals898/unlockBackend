from .models import *
from accounts.serializers import *
from rest_framework import serializers

class ResultSerializer(serializers.ModelSerializer):
    counselor_id = CounselorSerializer(read_only=True)

    class Meta:
        model = Result
        fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):
    result_id = ResultSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = "__all__"

