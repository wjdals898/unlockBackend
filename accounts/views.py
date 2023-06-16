from json import JSONDecodeError

import jwt
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import os

from .serializers import *

BASE_URL = 'http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'account/kakao/callback/'
KAKAO_LOGOUT_URI = BASE_URL + 'account/kakao/login/'

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


def kakao_login(request):
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code")


class KakaoLoginView(APIView):

    def post(self, request):
        # 리액트에서 장고로 kakao access code 보냄
        kakao_access_code = request.GET.get('code', None)
        print(f"code = {kakao_access_code}")

        # 프론트에서 kakao access code가 오지 않았을 경우
        if not kakao_access_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")

        # code로 access token 요청
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "redirect_uri": KAKAO_CALLBACK_URI,
            "code": kakao_access_code
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        token_response_json = requests.post(kakao_token_api, data=data).json()
        access_token = token_response_json.get('access_token')
        print(f"(1) kakao_access_token = {access_token}")

        # 에러 발생 시 중단
        error = token_response_json.get("error", None)
        print(f"(2) error = {error}")
        if error is not None:
            raise JSONDecodeError(error)

        # access token으로 카카오 계정 정보 가져오기
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded; charset=utf-8"
        }
        user_information = requests.get(url, headers=headers).json()
        print(f"(3) {user_information}")
        social_id = user_information.get("id")

        try:
            user = User.objects.get(social_id=social_id)
            print(f"105 line: {user.name}")
            social_user = SocialAccount.objects.filter(user=user).first()
            print(f"107 line: {social_user}")
            # 로그인
            if social_user:
                for token in OutstandingToken.objects.filter(user=user):
                    BlacklistedToken.objects.get_or_create(token=token)

                token = TokenObtainPairSerializer.get_token(user)
                # token = RefreshToken.for_user(user)
                data = {
                    'name': user.name,
                    'email': user.email,
                    #'gender': user.gender
                }
                res = Response({'user': data, 'refresh': str(token), 'access': str(token.access_token), "msg": "로그인 성공"}, status=status.HTTP_200_OK)
                res.set_cookie('access', str(token.access_token))
                res.set_cookie('refresh', str(token))
                return res

        except User.DoesNotExist:
            '''
            if user_information['kakao_account']['gender'] == "male":
                gender = "M"
            elif user_information['kakao_account']['gender'] == "female":
                gender = "F"
            else:
                gender = None
'''
            new_user = User.objects.create_user(
                email=user_information['kakao_account'].get('email', None),
                name=user_information['properties'].get('nickname'),
                social_id=social_id,
                #gender=gender,
            )
            new_user.set_unusable_password()
            new_user.save()

            SocialAccount.objects.create(
                user_id=new_user.id,
            )
            data = {
                'name': new_user.name,
                'email': new_user.email,
                'gender': new_user.gender
            }
            token = TokenObtainPairSerializer.get_token(new_user)
            # token = RefreshToken.for_user(new_user)
            res = Response({'user': data, 'refresh': str(token), 'access': str(token.access_token), "msg": "회원가입 성공"}, status=status.HTTP_201_CREATED)
            res.set_cookie('access', str(token.access_token))
            res.set_cookie('refresh', str(token))

            return res


class KakaoLogout(APIView):

    def get(self, request):
        admin_key = os.environ.get("KAKAO_ADMIN_KEY")
        kakao_logout_api = "https://kapi.kakao.com/v1/user/unlink"

        refresh = request.COOKIES.get('refresh')
        refresh_token = RefreshToken(refresh) # refresh token 정보 가져오기

        if not refresh_token:
            return Response({"err_msg": "유효하지 않거나 만료된 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(str(refresh_token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        social_id = user.social_id

        headers = {"Authorization": f"KakaoAK {admin_key}"}
        data = {"target_id_type": "user_id", "target_id": social_id}
        logout_response_json = requests.post(kakao_logout_api, headers=headers, data=data).json()

        response = logout_response_json.get("id")
        if social_id != response:
            return Response({"err_msg": "로그아웃 실패"})

        res = Response({'success': f"{response} 로그아웃 성공"}, status=status.HTTP_200_OK)

        for token in OutstandingToken.objects.filter(user_id=user_id):
            BlacklistedToken.objects.get_or_create(token=token)

        res.set_cookie('access', None)
        res.set_cookie('refresh', None)
        return res


class SignOutView(APIView):

    def delete(self, request, *args, **kwargs):
        kakao_signout_api = 'https://kapi.kakao.com/v1/user/unlink'
        admin_key = os.environ.get("KAKAO_ADMIN_KEY")

        token = request.headers.get('Authorization').split(' ')[1]
        print(token)
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)
        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            social_id = user.social_id

            headers = {"Authorization": f"KakaoAK {admin_key}"}
            data = {"target_id_type": "user_id", "target_id": social_id}
            logout_response_json = requests.post(kakao_signout_api, headers=headers, data=data).json()

            response = logout_response_json.get("id")
            if social_id != response:
                return Response({"err_msg": "회원탈퇴 실패"})

            user.delete()
            return Response({'msg': f"{user.name} 회원 탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'msg: 회원 없음'}, status=status.HTTP_404_NOT_FOUND)


class AuthAPIView(APIView):
    def get(self, request):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            if not token:
                return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

            payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)

            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            user_type = ""
            if Counselor.objects.filter(userkey_id=user_id): # 상담사
                user_type = "상담사"
            elif Counselee.objects.filter(userkey_id=user_id): # 내담자
                user_type = "내담자"
            else:
                return Response({'msg': '회원 유형 없음'}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(instance=user)
            data = {
                'social_id': serializer.data['social_id'],
                'email': serializer.data['email'],
                'name': serializer.data['name'],
                'gender': serializer.data['gender'],
                'type': user_type,
            }
            return Response(data, status=status.HTTP_200_OK)
        except jwt.exceptions.InvalidTokenError:
            res = Response({'err_msg': '사용불가토큰'}, status=status.HTTP_401_UNAUTHORIZED)
            return res


class UserTypeView(APIView):
    def post(self, request):
        user_type = request.data.get('user_type')
        access_token = request.headers.get('Authorization').split(' ')[1]
        refresh_token = request.headers.get('refresh')

        if not access_token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(access_token), SECRET_KEY, ALGORITHM)

        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)

        # Counselor일 경우
        if user_type == 0:
            new_counselor = Counselor.objects.create(
                userkey=user
            )
            data = {
                'counselor_id': new_counselor.id,
                'name': user.name,
                'email': user.email,
                'gender': user.gender,
            }
            return Response({'user': data, 'refresh': str(refresh_token), 'access': str(access_token), "msg": "상담사 회원가입 성공"}, status=status.HTTP_200_OK)
        # Counselee일 경우
        elif user_type == 1:
            new_counselee = Counselee.objects.create(
                userkey=user
            )
            data = {
                'counselee_id': new_counselee.id,
                'name': user.name,
                'email': user.email,
                'gender': user.gender
            }
            return Response({'user': data, 'refresh': str(refresh_token), 'access': str(access_token), "msg": "내담자 회원가입 성공"}, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "상담사 또는 내담자를 선택하세요"}, status=status.HTTP_400_BAD_REQUEST)


class CounselorView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        print(token)
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        if Counselor.objects.filter(userkey_id=user_id).exists():
            counselor = Counselor.objects.get(userkey_id=user_id)
            serializer = CounselorSerializer(instance=counselor)
            data = {
                'counselor_id': serializer.data['id'],
                'social_id': serializer.data['userkey']['social_id'],
                'email': serializer.data['userkey']['email'],
                'name': serializer.data['userkey']['name'],
                'gender': serializer.data['userkey']['gender'],
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "상담사가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


class CounseleeView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        print(token)
        if not token:
            return Response({"err_msg": "토큰 없음"}, status=status.HTTP_200_OK)

        payload = jwt.decode(str(token), SECRET_KEY, ALGORITHM)
        user_id = payload.get('user_id')

        if Counselee.objects.filter(userkey_id=user_id).exists():
            counselee = Counselee.objects.get(userkey_id=user_id)
            serializer = CounseleeSerializer(instance=counselee)
            data = {
                'id': serializer.data['id'],
                'social_id': serializer.data['userkey']['social_id'],
                'email': serializer.data['userkey']['email'],
                'name': serializer.data['userkey']['name'],
                'gender': serializer.data['userkey']['gender'],
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "내담자가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
