from django.urls import path
from . import views

urlpatterns = [
    path('diem-danh/', views.danh_sach_diem_danh, name='danh_sach_diem_danh'),
    path('diem-danh/them/', views.them_diem_danh, name='them_diem_danh'),
]
