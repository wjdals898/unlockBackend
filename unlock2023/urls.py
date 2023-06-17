import rest_framework
from django.urls import path, include
from .views import *


app_name = 'unlock2023'

urlpatterns = [
    path('', ReservationListAPIView.as_view()),
    path('reservationdetail/', ReservationEditAPIView.as_view())
]