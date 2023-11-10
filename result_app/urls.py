from django.urls import path
from .views import *

app_name = "result_app"

urlpatterns = [
    path('counselee/', CounseleeListView.as_view()),
    path('result/', ResultListView.as_view()),
    path('result/pres/', PrescriptionListView.as_view()),
    path('result/pres/detail/', PrescriptionDetail.as_view()),
    path('video/', VideoView.as_view()),
    # path('csv_file/', CSVFileDownloadView.as_view()),
    path('result_file_download/', ResultFileDownloadView.as_view()),
]
