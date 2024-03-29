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
from django.shortcuts import render
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from Backend.settings import DEBUG

admin.site.site_header = '0xFLOOR 后台'
admin.site.site_title = '0xFLOOR 后台'
admin.site.index_title = '0xFLOOR 后台'

schema_view = get_schema_view(
    openapi.Info(
        title="0xFLOOR项目 API",
        default_version="版本 v1.0.0",
        description="0xFLOOR项目API交互文档由Swagger自动生成",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/v1/user/', include('User.urls')),
    path('api/v1/mining-machine-product/', include('MiningMachineProduct.urls')),
    path('api/v1/order/', include('Order.urls'))
]

if DEBUG:
    urlpatterns.append(path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'))
    urlpatterns.append(path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'))
