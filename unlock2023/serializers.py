from rest_framework import serializers
from accounts.serializers import CounselorSerializer, CounseleeSerializer, UserSerializer
from .models import Reservation, Counselor, Counselee, CounselingType, Counselor_list


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

class CounselorlistSerializer(serializers.ModelSerializer):
    counselorlist_id = serializers.SerializerMethodField()
    counselorlist_name = serializers.SerializerMethodField()
    counselorlist_prof_field = serializers.SerializerMethodField()

    def get_counselorlist_id(self, obj):
        Counselor = obj.c_id
        return Counselor.id

    def get_counselorlist_name(self, obj):
        Counselor = obj.c_id
        user = Counselor.userkey
        return user.name

    def get_counselorlist_prof_field(self, obj):
        CounselingType = obj.prof_field
        return CounselingType.type

    class Meta:
        model = Counselor_list
        fields = ['c_id', 'counselorlist_id','counselorlist_name', 'institution_name', 'institution_address', 'credit', 'prof_field', 'counselorlist_prof_field']