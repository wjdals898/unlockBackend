import csv
import json
from io import StringIO

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework.parsers import FileUploadParser, MultiPartParser

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
import boto3
import os
from django.http import HttpResponse

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
                cseInformation[n] = {"id":serial["id"], "name": serial["userkey"]["name"],
                                                "email": serial["userkey"]["email"], "gender": serial["userkey"]["gender"],
                                                "birth": serial["userkey"]["birth"]}
                n += 1

            return Response(json.dumps(cseInformation))
        else:
            return Response({"msg": "상담사가 아니면 볼 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 위에서 선택한 내담자의 결과 리스트 뽑기
class ResultListView(APIView):
    parser_classes = [MultiPartParser, ]

    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)
        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        print(user_id)
        
        if Counselor.objects.filter(userkey=user_id).exists():
            counselor_id = Counselor.objects.get(userkey=user_id)
            print("counselor_id = ", counselor_id)
            try:
                #print("counselee_id = ", request.GET.get('id'))
                results = Result.objects.filter(counselor_id=counselor_id.id).all() #, counselee_id=request.GET.get('id')
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
                video=request.FILES.get('video')
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


class VideoView(APIView):
    parser_classes = [MultiPartParser, ]
    def post(self, request, format=None):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        print("counselee_id = ", request.data.get('counselee_id'))
        print(user_id)
        print(request.FILES)
        print(request.data.get("video"))
        if request.data.get('video'):
            print(request.FILES['video'])

        # 상담사 계정에서 내담자 결과가 있을 경우 동영상 업로드
        if Counselor.objects.filter(userkey=user_id).exists():
            print("상담사가 맞습니다.")
            counselor = Counselor.objects.get(userkey=user_id)
            if Result.objects.filter(counselor=counselor).exists():
                result = Result.objects.get(counselor=counselor)
                print(result)
                result.video = request.FILES.get('video')
                result.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CSVFileDownloadView(APIView):
    def get(self, request):
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        s3_bucket_name = os.environ.get('AWS_RESULT_STORAGE_BUCKET_NAME')

        # AWS S3 클라이언트 초기화
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

        # S3에서 CSV 파일 다운로드
        s3_object_key = 'emotion_mean/c2_r18_emotion_mean.csv'
        response = s3.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
        csv_file = response['Body'].read().decode('utf-8')

        csv_reader = csv.DictReader(StringIO(csv_file))

        new_csvfile = None
        for row in csv_reader:
            new_csvfile = CSVFile.objects.create(
                emotion1=row['Happymean'],
                emotion2=row['Surprisemean'],
                emotion3=row['Expressionlessmean'],
                emotion4=row['Fearmean'],
                emotion5=row['Aversionmean'],
                emotion6=row['Angrymean'],
                emotion7=row['Sadmean'],
            )
        serializer = CSVFileSerializer(new_csvfile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultFileDownloadView(APIView):
    def post(self, request):
        file_type = request.data.get('type') # 1은 emotion_mean / 2는 mind / 3은 행동
        c_id = request.data.get('c_id')
        print(c_id)
        r_id = request.data.get('r_id')
        print(r_id)
        s3 = boto3.client('s3')
        bucket_name = os.environ.get('AWS_RESULT_STORAGE_BUCKET_NAME')
        file_key = ""
        if file_type == 1:
            print("평균 감정 다운")
            file_key = f"emotion_mean/c{c_id}_r{r_id}_emotion_mean.csv"
        elif file_type == 2:
            print("마인드 다운")
            file_key = f"mind/c{c_id}_r{r_id}_node_positions_with_emotion.csv"
        elif file_type == 3:
            print("행동 다운")
            file_key = f"movement_result/c{c_id}_r{r_id}_movements_data.csv"
        elif file_type == 4:
            print("전체 감정 다운")
            file_key = f"emotion_result/c{c_id}_r{r_id}_emotion_results.csv"
        else:
            file_key = ""

        print("file_key ", file_key)

        try:
            print('bucket : ', bucket_name)
            print('file_key : ', file_key)
            response1 = s3.get_object(Bucket=bucket_name, Key=file_key)
            print('response1 : ', response1)

            # 파일 내용 읽기
            csv_content = response1['Body'].read().decode('utf-8')
            print(csv_content)

            print("s3 다운하기")
            http_response = HttpResponse(csv_content)
            http_response['Content-Disposition'] = f'attachment; filename="c{c_id}_r{r_id}_result{file_type}.csv"'

            print('http_response : ', http_response)

            return http_response

        except Exception as e:
            return Response("Failed to download CSV file from S3: " + str(e), status=500)