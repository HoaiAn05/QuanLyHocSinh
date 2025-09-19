"""
URL configuration for student_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from accounts.views import home
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # verify token
    path('admin/', admin.site.urls),

    # API cho từng app
    path("", home, name="home"),
    path('', include('students.urls')),
    path('', include('notifications.urls')),
    path('', include('scores.urls')),
    path('', include('accounts.urls')),
    path('', include('classes.urls')),
    path('', include('subjects.urls')),
    path('', include('teachers.urls')),
    path('', include('attendance.urls')),
]
