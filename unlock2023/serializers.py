from rest_framework import serializers

from accounts.serializers import CounselorSerializer, CounseleeSerializer
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    #counselor_id = CounselorSerializer(read_only=True)
    #counselee_id = CounseleeSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = ['counselor_id', 'counselee_id', 'date', 'time', 'type']