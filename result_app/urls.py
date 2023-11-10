from django.urls import path
from .views import *

app_name = "result_app"

urlpatterns = [
    path('counselee/', CounseleeListView.as_view()),
    path('result/', ResultListView.as_view()),
    path('result/pres/', PrescriptionListView.as_view()),
    path('result/pres/detail/', PrescriptionDetail.as_view()),
    path('video/', VideoView.as_view()),
<<<<<<< HEAD
    # path('csv_file/', CSVFileDownloadView.as_view()),
=======
    #path('csv_file/', CSVFileDownloadView.as_view()),
>>>>>>> 89f2385039a400d5b3448599e72d1adb73930e9c
    path('result_file_download/', ResultFileDownloadView.as_view()),
]






'''
path("prescription/<int:result_id>/", views.pres_view, name="pres_view"),   # 결과 ID 받기
    path("prescription/add/<int:result_id>/", views.add_pres, name="add_pres"), 
    path("prescription/update/<int:pres_id>/", views.update_pres, name="update_pres"),  # 처방전 ID 받기
    path("prescription/delete/<int:pres_id>/", views.delete_pres, name="delete_pres"),

'''