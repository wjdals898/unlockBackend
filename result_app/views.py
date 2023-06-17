from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from accounts.serializers import CounseleeSerializer
from .models import Result, Prescription
from accounts.models import Counselor, Counselee
from django.db.models import Q
from .forms import PresForm
from datetime import datetime
from django.contrib import messages
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from rest_framework import status, generics

import os

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

# Create your views here.

# 내담자 List
class CounseleeListView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)
        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        counselor_id = Counselor.objects.get(userkey=user_id)

        cse = Result.objects.filter(counselor_id=counselor_id.id).values_list('counselee', flat=True).distinct().order_by("counselor_id")
        counselee_id = cse.values()[0].get('counselee_id')
        counselee = Counselee.objects.filter(id=counselee_id)
        print(counselee.values())
        print(cse.values()[0].get('counselee_id'))
        serializer = CounseleeSerializer(instance=counselee, many=True)
        return Response(serializer.data)


# 위에서 선택한 내담자의 결과 리스트 뽑기
class ResultListView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)
        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        counselor_id = Counselor.objects.get(userkey=user_id)

        results = Result.objects.filter(counselor_id=counselor_id.id, counselee_id=request.data['id']).all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

    def post(self, request):
        # request.data에 counselee_id와 video_url, analysis_url 3개 들어있음
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        counselor_id = Counselor.objects.get(userkey=user_id)

        if Counselor.objects.filter(id=counselor_id.id).exists():
            counselor = Counselor.objects.get(id=counselor_id.id)

            counselee_id = request.data.get('counselee_id')
            if Counselee.objects.filter(id=counselee_id).exists():
                counselee = Counselee.objects.get(id=counselee_id)
                new_result = Result.objects.create(
                    counselor=counselor,
                    counselee=counselee,
                    video_url=request.data['video_url'],
                    analysis_url=request.data['analysis_url']
                )

                serializer = ResultSerializer(new_result)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": "결과 저장 불가 (내담자 존재하지 않음)"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "결과 저장 불가 (상담사 존재하지 않음)"}, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionListView(APIView):

    # 결과에 해당하는 처방전
    def get(self, request):
        try:
            pres = Prescription.objects.get(result_id=request.data['id'])
            serializer = PrescriptionSerializer(pres)
            return Response(serializer.data)

        except:
            return Response({'msg': '처방전이 존재하지 않습니다.'})

    # 처방전 추가
    def post(self, request):
        result_id = request.data.get('result_id')
        pres = request.data.get('content')

        if Result.objects.filter(id=result_id).exists():
            result = Result.objects.get(id=result_id)

            new_pres = Prescription.objects.create(
                result=result,
                content=pres
            )

            serializer = PrescriptionSerializer(new_pres)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": "처방전 저장 불가"}, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionDetail(APIView):
    authentication = [JWTAuthentication]

    # 처방전 수정
    def put(self, request):
        try:
            pres = Prescription.objects.get(id=request.data['id'])
            print(pres.result_id)

            serializer = PrescriptionSerializer(instance=pres, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Prescription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # 처방전 삭제
    def delete(self, request):
        try:
            pres = Prescription.objects.get(id=request.data['id'])
            pres.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Prescription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)