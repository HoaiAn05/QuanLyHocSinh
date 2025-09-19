from django.urls import path
from . import views

urlpatterns = [
    # CRUD lớp học
    path("lop/", views.lop_list, name="lop_list"),
    path("lop/add/", views.lop_create, name="lop_create"),
    path("lop/<int:pk>/update/", views.lop_update, name="lop_update"),
    path("lop/<int:pk>/delete/", views.lop_delete, name="lop_delete"),

    # Chi tiết lớp học
    path("lop-detail/<int:pk>/", views.lop_detail, name="lop_detail"),

    # Quản lý học sinh trong lớp (chỉ dùng học sinh có sẵn)
    path("lop/<int:pk>/add-student/", views.add_student_to_class, name="add_student_to_class"),
    path("lop/<int:pk>/remove-student/<int:student_id>/", views.remove_student_from_class, name="remove_student_from_class"),
    path("lop/<int:pk>/student/<int:student_id>/edit/", views.student_update, name="student_update"),

    path("phancong/", views.phancong_list, name="phancong_list"),
    path("phancong/add/", views.phancong_add, name="phancong_add"),
    path("phancong/<int:pk>/edit/", views.phancong_edit, name="phancong_edit"),
    path("phancong/<int:pk>/delete/", views.phancong_delete, name="phancong_confirm_delete"),
]
