import os

import jwt
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import SelfCheck
from .serializers import *
from rest_framework.views import APIView

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


class SelfCheckList(APIView):
    authentication = [JWTAuthentication]
    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)
        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        try:
            counselee_id = Counselee.objects.get(userkey_id=user_id)
            selfcheck = SelfCheck.objects.filter(counselee_id=counselee_id)

            serializer = SelfCheckSerializer(selfcheck, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except SelfCheck.DoesNotExist:
            return Response({'msg': f'{user_id}의 일기장이 존재하지 않습니다.'})

    def post(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        if Counselee.objects.filter(userkey_id=user_id).exists():
            counselee = Counselee.objects.get(userkey_id=user_id)

            new_selfcheck = SelfCheck.objects.create(
                counselee_id=counselee,
                public_yn=request.data.get('public_yn'),
                video_url=request.data.get('video_url'),
                analysis_url=request.data.get('analysis_url')
            )

            serializer = SelfCheckSerializer(new_selfcheck)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": "일기장 저장 불가"}, status=status.HTTP_400_BAD_REQUEST)


def selfCheck(s_id):
    try:
        selfcheck = SelfCheck.objects.get(id=s_id)
        print(selfcheck)
    except SelfCheck.DoesNotExist:
        return None
    return selfcheck


class SelfCheckDetail(APIView):
    authentication = [JWTAuthentication]

    def get(self, request):
        selfcheck = selfCheck(request.data['id'])

        if selfcheck == None:
            return Response({"msg": "일기장이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SelfCheckSerializer(selfcheck)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        selfcheck = selfCheck(request.data['id'])

        serializer = SelfCheckSerializer(instance=selfcheck, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        selfcheck = selfCheck(request.data['id'])

        selfcheck.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
