import os

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import *
from .serializers import *

# Create your views here.

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


class ReservationListAPIView(APIView):
    authentication = [JWTAuthentication]

    # 모든 예약정보 나열
    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)
        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        try:
            reservations = None
            if Counselor.objects.filter(userkey_id=user_id).exists():
                counselor_id = Counselor.objects.get(userkey_id=user_id)
                print(f"line32: {counselor_id}")
                reservations = Reservation.objects.filter(Counselor_id=counselor_id)
                print(f"line34: {reservations}")
            elif Counselee.objects.filter(userkey_id=user_id).exists():
                counselee_id = Counselee.objects.get(userkey_id=user_id)
                print(f"line32: {counselee_id}")
                reservations = Reservation.objects.filter(Counselee_id=counselee_id)
                print(f"line34: {reservations}")
            serializer = ReservationSerializer(reservations, many=True)

            return Response(serializer.data)

        except Reservation.DoesNotExist:
            return Response({'msg': f'예약 내역이 없습니다.'})

    def post(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        data = request.data.get('data')
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        if Reservation.objects.filter(date=data.get('date'), time=data.get('time')).exists():
            return Response({'error': '예약할 수 없습니다.'}, status=400)

        if Counselee.objects.filter(userkey_id=user_id).exists():
            counselee = Counselee.objects.get(userkey_id=user_id)
            counselor = Counselor.objects.get(id=data.get('counselor_id'))

            new_reservation = Reservation.objects.create(
                Counselee_id=counselee,
                Counselor_id=counselor,
                date=data.get('date'),
                time=data.get('time'),
                type=data.get('type')
            # 다른 예약 정보 필드 설정
            )

            serializer = ReservationSerializer(new_reservation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"msg": "예약 생성 불가"}, status=status.HTTP_400_BAD_REQUEST)


def reservation(s_id):
    try:
        reservation = Reservation.objects.get(id=s_id)
    except Reservation.DoesNotExist:
        return Response({"msg": "해당 예약 정보 없음"}, status=status.HTTP_404_NOT_FOUND)
    return reservation


# 포스팅 내용, 수정, 삭제
class ReservationEditAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    # 특정 예약 정보 가져오기
    def get(self, request):
        reser = reservation(request.data['id'])

        serializer = ReservationSerializer(reser)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 특정 예약 정보 삭제
    def delete(self, request):
        reser = reservation(request.data['id'])
        reser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
