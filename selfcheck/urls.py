from django.urls import path, include
from .views import *


urlpatterns = [
    path('', SelfCheckList.as_view(), name="selfcheck_list"),
    path('detail/', SelfCheckDetail.as_view(), name="selfcheck_one"),
]