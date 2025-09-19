from django.urls import path
from . import views

urlpatterns = [
    path("chon-lop/", views.chon_lop_nam_hoc, name="chon_lop_nam"),
    path("nhap-diem/<int:lop_id>/", views.nhap_diem_lop, name="nhap_diem_lop"),
    path("xem-bang-diem-lop/<int:lop_id>/", views.xem_bang_diem_lop, name="xem_bang_diem_lop"),


    path("chon-nam-hoc-hoc-ky/", views.chon_hoc_ky_hs, name="chon_hoc_ky_hs"),
    path("bang-diem/", views.xem_bang_diem_hoc_sinh, name="xem_bang_diem_hoc_sinh"),

    path("bao-cao-diem/", views.bao_cao_diem, name="bao_cao_diem"),
]
