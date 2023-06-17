from .models import *
from rest_framework import serializers
from result_app.serializers import ResultSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'social_id',
            'email',
            'gender',
            'is_superuser',
            'is_active',
            'is_staff',
            'created_at',
            'updated_at',
            #'counselor_id',
            #'counselee_id'
        ]


class CounselorSerializer(serializers.ModelSerializer):
    result_id = ResultSerializer(read_only=True, required=False, many=True)
    userkey = UserSerializer(read_only=True)

    class Meta:
        model = Counselor
        fields = [
            'id',
            'userkey',
            'result_id'
        ]


class CounseleeSerializer(serializers.ModelSerializer):
    result_id = ResultSerializer(read_only=True, required=False, many=True)
    #selfcheck_id = SelfCheckSerializer(read_only=True, many=True, required=False)
    userkey = UserSerializer(read_only=True)

    class Meta:
        model = Counselee
        fields = [
            'id',
            'userkey',
            'result_id',
            #'selfcheck_id',
        ]


