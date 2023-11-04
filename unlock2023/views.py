import os

import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .models import *

# Create your views here.

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


class ReservationAllListView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)
        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        if Counselee.objects.filter(userkey=user_id).exists():  # 내담자 계정일 경우
            topic = request.GET.get('topic')
            print(topic)
            counselee = Counselee.objects.get(userkey=user_id)
            reservations = Reservation.objects.filter(type=topic, counselee_id=counselee)
            serializer = ReservationSerializer(reservations, many=True)
            print(serializer.data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif Counselor.objects.filter(userkey=user_id).exists():    # 상담사 계정일 경우
            counselor = Counselor.objects.get(userkey=user_id)
            reservations = Reservation.objects.filter(counselor_id=counselor)
            serializer = ReservationSerializer(reservations, many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:   # 둘 다 아닐 경우 예외 처리
            return Response({}, status=status.HTTP_204_NO_CONTENT)


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
                reservations = Reservation.objects.filter(counselor_id=counselor_id)

                print(f"line34: {reservations}")
            elif Counselee.objects.filter(userkey_id=user_id).exists():
                counselee_id = Counselee.objects.get(userkey_id=user_id)
                print(f"line32: {counselee_id}")
                reservations = Reservation.objects.filter(counselee_id=counselee_id)
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
        print(user_id)
        print(payload)

        if Reservation.objects.filter(date=data.get('date'), time=data.get('time'), counselor_id=data.get('counselor_id')).exists():
            return Response({'error': '예약할 수 없습니다.'}, status=400)

        if Counselee.objects.filter(userkey_id=user_id).exists():
            counselee = Counselee.objects.get(userkey_id=user_id)
            print(Counselee.userkey)
            counselor = Counselor.objects.get(id=data.get('counselor_id'))
            type_id = CounselingType.objects.get(id=data.get('type'))

            new_reservation = Reservation.objects.create(
                counselee_id=counselee,
                counselor_id=counselor,
                date=data.get('date'),
                time=data.get('time'),
                type=type_id
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
        print(reser)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 특정 예약 정보 삭제
    def delete(self, request):

        reser = reservation(request.data['id'])
        reser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Counselor_listAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    #상담사 리스트 가져오기
    def get(self, request):
        list = Counselor.objects.all()
        serializer = CounselorSerializer(list, many=True)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #상담사 개인 정보 입력하기
    def post(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        data = request.data.get('data')
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        print(user_id)
        print(payload)

        if Counselor.objects.filter(userkey_id=user_id).exists():
            return Response({"msg": "상담자로 등록할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(id=user_id)
            print(user)
            user_table_id = user.id
            print(user_table_id)
            counselor = Counselor.objects.get(userkey_id=user_table_id)
            print(counselor)
            user = counselor.userkey
            counselorlist_name = user.name
            print(counselorlist_name)
            prof = CounselingType.objects.get(type=data.get('prof_field'))
            n_l = Counselor.objects.create(
                userkey=user,
                institution_name=data.get('institution_name'),
                institution_address=data.get('institution_address'),
                credit=data.get('credit'),
                prof_field=prof
            )
            serializer = ReservationSerializer(n_l)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)