
# classes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("teacher/", views.teacher_list, name="teacher_list"),
    path("teacher/add/", views.teacher_add, name="teacher_add"),
    path("teacher/<int:pk>/edit/", views.teacher_edit, name="teacher_edit"),
    path("teacher/<int:pk>/delete/", views.teacher_delete, name="teacher_delete"),

    path("profile/", views.giao_vien_profile, name="giao_vien_profile"),
    path("doi-mat-khau/", views.doi_mat_khau, name="doi_mat_khau"),

    path('lich-day/', views.xem_lich_day, name='xem_lich_day')
]

