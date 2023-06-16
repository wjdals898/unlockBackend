import rest_framework
from django.urls import path, include, admin

app_name = 'unlock2023'
urlpatterns = [
        path('admin/', admin.site.urls),
    path('', include('rest_framework.urls'))
]