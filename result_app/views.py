import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from accounts.serializers import CounseleeSerializer
from .models import Result, Prescription
from accounts.models import Counselor, Counselee
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

        if Counselor.objects.filter(userkey=user_id).exists():
            counselor = Counselor.objects.get(userkey=user_id)

            cse = Result.objects.filter(counselor_id=counselor.id).values_list('counselee', flat=True).distinct().order_by("counselor_id")

            counselee_id = cse.values()[0].get('counselee_id')

            lst = []
            for c in cse.values():
                lst.append(c["counselee_id"])
            counselee_id = list(set(lst))

            counselee = Counselee.objects.filter(id__in=counselee_id)
            serializer = CounseleeSerializer(instance=counselee, many=True)

            cseInformation = [0] * len(serializer.data)
            n = 0
            for serial in serializer.data:
                cseInformation[n] = {"id":serial["id"]}
                cseInformation[n]["userkey"] = {"id": serial["userkey"]["id"], "name": serial["userkey"]["name"],
                                                "email":serial["userkey"]["email"], "gender": serial["userkey"]["gender"]}
                n += 1

            return Response(json.dumps(cseInformation))
        else:
            return Response({"msg": "상담사가 아니면 볼 수 없습니다."})


# 위에서 선택한 내담자의 결과 리스트 뽑기
class ResultListView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)
        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        
        if Counselor.objects.filter(userkey=user_id).exists():
            counselor_id = Counselor.objects.get(userkey=user_id)
            
            try:
                results = Result.objects.filter(counselor_id=counselor_id.id, counselee_id=request.data['id']).all()
                serializer = ResultSerializer(results, many=True)
                return Response(serializer.data)
            except:
                Response({"msg": "결과가 존재하지 않습니다"})
        elif Counselee.objects.filter(userkey=user_id).exists():
            counselee_id = Counselee.objects.get(userkey=user_id)
            
            try:
                results = Result.objects.filter(counselee_id=counselee_id.id)
                serializer = ResultSerializer(results, many=True)
                return Response(serializer.data)
            except:
                return Response({"msg": "결과가 존재하지 않습니다"})

    def post(self, request):
        # request.data에 counselee_id와 video_url, analysis_url 3개 들어있음
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        
        # 상담사일 때
        if Counselor.objects.filter(userkey=user_id).exists():
            counselor = Counselor.objects.get(userkey=user_id)

            counselee_id = request.data.get('counselee_id')
            if Counselee.objects.filter(id=counselee_id).exists():
                counselee = Counselee.objects.get(id=counselee_id)
            else:
                return Response({"msg": "결과 저장 불가 (내담자 존재하지 않음)"}, status=status.HTTP_400_BAD_REQUEST)
        # 내담자일 때
        elif Counselee.objects.filter(userkey=user_id):
            counselee = Counselee.objects.get(userkey=user_id)

            counselor_id = request.data.get('counselor_id')
            if Counselor.objects.filter(id=counselor_id).exists():
                counselor = Counselor.objects.get(id=counselor_id)
            else:
                return Response({"msg": "결과 저장 불가 (상담사 존재하지 않음)"}, status=status.HTTP_400_BAD_REQUEST)
        # 상담사도 내담자도 아닐 때
        else:
            return Response({"msg": "사용자 정보에서 상담사인지 내담자인지 선택해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_result = Result.objects.create(
                counselor=counselor,
                counselee=counselee,
                video_url=request.data['video_url'],
                analysis_url=request.data['analysis_url']
            )

            serializer = ResultSerializer(new_result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"msg": "결과 저장 불가"}, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionListView(APIView):

    # 결과에 해당하는 처방전
    def get(self, request):
        try:
            pres = Prescription.objects.get(result=request.data['id'])
            serializer = PrescriptionSerializer(pres)
            return Response(serializer.data)

        except:
            return Response({'msg': '처방전이 존재하지 않습니다.'})

    # 처방전 추가
    def post(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        
        # 상담사일 때만 작성
        if Counselor.objects.filter(userkey=user_id).exists():
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
        else:
            return Response({"msg": "처방전 저장 불가 (상담사만 처방전을 작성할 수 있습니다"}, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionDetail(APIView):
    authentication = [JWTAuthentication]

    # 처방전 수정
    def put(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        # 상담사일 때만 수정
        if Counselor.objects.filter(userkey=user_id).exists():
        
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
        else:
            return Response({"msg": "처방전 저장 불가 (상담사만 처방전을 수정할 수 있습니다"}, status=status.HTTP_400_BAD_REQUEST)

    # 처방전 삭제
    def delete(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        # 상담사일 때만 삭제
        if Counselor.objects.filter(userkey=user_id).exists():
            try:
                pres = Prescription.objects.get(id=request.data['id'])
                pres.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Prescription.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"msg": "처방전 저장 불가 (상담사만 처방전을 삭제할 수 있습니다"}, status=status.HTTP_400_BAD_REQUEST)