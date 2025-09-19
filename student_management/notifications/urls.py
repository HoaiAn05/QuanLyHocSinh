from django.urls import path
from . import views


urlpatterns = [
    path('thong-bao/', views.danh_sach_thong_bao, name='danh_sach_thong_bao'),
    path('thong-bao/gui/', views.gui_thong_bao, name='gui_thong_bao'),
    path('<int:id>/', views.chi_tiet_thong_bao, name='chi_tiet_thong_bao'),
    path('<int:id>/xoa/', views.xoa_thong_bao, name='xoa_thong_bao'),
]
