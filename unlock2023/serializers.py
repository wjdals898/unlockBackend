from rest_framework import serializers

from accounts.serializers import CounselorSerializer, CounseleeSerializer
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['Counselor_id', 'Counselee_id', 'date', 'time', 'type']