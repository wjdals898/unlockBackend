from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CounselorSerializer(serializers.ModelSerializer):
    userkey = UserSerializer(many=False, required=True)

    class Meta:
        model = Counselor
        fields = '__all__'


class CounseleeSerializer(serializers.ModelSerializer):
    userkey = UserSerializer(many=False, required=True)

    class Meta:
        model = Counselee
        fields = '__all__'
