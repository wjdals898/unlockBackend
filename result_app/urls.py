from django.urls import path
from . import views

app_name = "result_app"

urlpatterns = [
    path('result/<int:cse_id>/', views.result_view, name="result_view"),    # 내담자 ID 받기
    path("prescription/<int:result_id>/", views.pres_view, name="pres_view"),   # 결과 ID 받기
    path("prescription/add/<int:result_id>/", views.add_pres, name="add_pres"), 
    path("prescription/update/<int:pres_id>/", views.update_pres, name="update_pres"),  # 처방전 ID 받기
    path("prescription/delete/<int:pres_id>/", views.delete_pres, name="delete_pres"),
    
]