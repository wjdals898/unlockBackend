from rest_framework import serializers
from accounts.serializers import CounselorSerializer, CounseleeSerializer, UserSerializer
from .models import Reservation, Counselor, Counselee


class ReservationSerializer(serializers.ModelSerializer):
    counselor_name = serializers.SerializerMethodField()
    counselee_name = serializers.SerializerMethodField()
    type_name = serializers.SerializerMethodField()

    def get_counselee_name(self, obj):
        Counselee = obj.counselee_id
        user = Counselee.userkey
        return user.name

    def get_counselor_name(self, obj):
        Counselor = obj.counselor_id
        user = Counselor.userkey
        return user.name

    def get_type_name(self, obj):
        CounselingType = obj.type
        return CounselingType.type
    class Meta:
        model = Reservation
        fields = ['counselor_id', 'counselee_id', 'counselor_name', 'counselee_name', 'date', 'time', 'type', 'type_name']