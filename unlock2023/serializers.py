from rest_framework import serializers
from .models import Counselor, Counselee, Reservation
from accounts.serializers import CounseleeSerializer, CounselorSerializer


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['Counselor_id', 'Counselee_id', 'date', 'time', 'type']