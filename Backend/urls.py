"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework import routers
from django.conf import settings

from unlock2023 import views

from rest_framework_swagger.views import get_swagger_view

import accounts.api

from unlock2023 import views

app_name = 'accounts'

router = routers.DefaultRouter()
router.register('users', accounts.api.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("result_app.urls")),
    re_path(r'^api/doc/', get_swagger_view(title='Rest API Document')),
    re_path(r'^api/v1/', include((router.urls, 'accounts'), namespace='api')),
    path('account/', include('accounts.urls')),
    path('account/', include('allauth.urls')),
    path('selfcheck/', include('selfcheck.urls')),
    path('reservation/', include('unlock2023.urls')),
    path('reservation/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
