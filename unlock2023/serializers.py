from rest_framework import serializers
from .models import Counselor, Counselee, Reservation

class CounselorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counselor
        fields = ['user_id1']

class CounseleeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counselee
        fields = ['user_id2']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['Counselor_id', 'Counselee_id', 'date', 'time', 'type']