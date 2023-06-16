from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Result, Prescription
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

        cse = Result.objects.filter(counselor_id=counselor_id['id']).order_by("counselor_id").distinct()
        serializer = ResultSerializer(cse, many=True)
        return Response(serializer.data)


# 내담자 선택 후 내담자 결과 리스트 뽑기
class ResultListView(APIView):

    def get(self, request, cseId):
        results = Result.objects.filter(counselor_id=request.data['id'], counselee_id=cseId).all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ResultSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)






# 결과 ID 받아서 해당 결과의 처방전 보여주기
def pres_view(request, result_id):
    # 처방전 있으면 보여주기
    pres = get_object_or_404(Prescription, result_id=result_id)
    return render(request, 'result_app/prescription.html', context={'pres':pres})

# 결과 ID 받아서 해당 결과의 처방전 작성하기
def add_pres(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    if request.method == 'POST':
        form = PresForm(request.POST)

        if form.is_valid():  # 유효하면 처방전 내용 추가
            comment = form.save(commit=False)
            comment.result_id = result
            comment.save()
            return redirect("result_app:pres_view", result_id)  
    else:
        form = PresForm()
    return render(request, 'result_app/pres_form.html', context={'result':result, 'form':form})

# 처방전 ID 받아서 처방전 수정하기
def update_pres(request, pres_id):
    pres = get_object_or_404(Prescription, id=pres_id)

    if request.method == "POST":
        form = PresForm(request.POST, instance=pres)
        if form.is_valid():
            form.save()
            return redirect('result_app:pres_view', pres.result_id)
    else:
        form = PresForm(instance=pres)
    return render(request, 'result_app/pres_form', context={'pres':pres, 'form':form})

# 처방전 ID 받아서 처방전 삭제하기
def delete_pres(request, pres_id):
    pres = get_object_or_404(Prescription, id=pres_id)
    pres.delete()
    return redirect('result_app:pres_view', pres.result_id)