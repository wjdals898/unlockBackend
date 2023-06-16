from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('kakao/login/', kakao_login, name='kakao_login'),  # 카카오 인가 코드(프론트 구현하면 삭제)
    path('kakao/callback/', KakaoLoginView.as_view(), name='kakao_login_todjango'),    # 카카오 로그인 & 회원가입
    path('kakao/logout/', KakaoLogout.as_view(), name='kakao_logout'),  # 로그아웃
    path('signout/', SignOutView.as_view(), name='signout'),
    path('auth/', AuthAPIView.as_view(), name='auth'),  # 회원 확인(상담사인지 내담자인지도 확인 가능)
    path('usertype/', UserTypeView.as_view(), name='user_type'),    # 카카오 회원가입 후 회원 유형 선택 시 연결
    path('counselor/', CounselorView.as_view(), name='counselor'),
    path('counselee/', CounseleeView.as_view(), name='counselee'),
    path('token/refresh/', TokenRefreshView.as_view()),    # 토큰 재발급하기
]
