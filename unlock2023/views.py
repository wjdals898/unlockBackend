from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ReservationListAPIView(APIView):
    #모든 예약정보 나열
    def get(self, request):
        serializer = ReservationSerializer(Reservation.objects.all(), many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']
            
            # 중복 여부 확인
            if Reservation.objects.filter(date=date, time=time).exists():
                return Response({'error': '중복된 값입니다.'}, status=400)
            
            # 중복이 없을 경우 예약 생성
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

from django.shortcuts import get_object_or_404

# 포스팅 내용, 수정, 삭제
class ReservationEditAPIView(APIView):
    #pk값을 이용하여 특정 예약 객체를 데이터베이스에서 가져오기
    def get_object(self, pk):
        return get_object_or_404(Reservation, pk=pk)
    #특정 예약 정보 가져오기
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = ReservationSerializer(post)
        return Response(serializer.data)
    # 특정 예약 정보 수정
    def put(self, request, pk):
        Reservation = self.get_object(pk)
        serializer = ReservationSerializer(Reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 특정 예약 정보 삭제
    def delete(self, request, pk):
        Reservation = self.get_object(pk)
        Reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)