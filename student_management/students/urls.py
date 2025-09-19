# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_list, name='student_list'),
    path('student/add/', views.student_add, name='student_add'),
    path('student/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('student/<int:pk>/assign/', views.assign_classroom, name='assign_classroom'),

    path("tkb/", views.tkb_list, name="tkb_list"),
    path("tkb/create/", views.tkb_create, name="tkb_create"),
    path("tkb/update/<int:pk>/", views.tkb_update, name="tkb_update"),
    path("tkb/delete/<int:pk>/", views.tkb_delete, name="tkb_delete"),

    path('thoi-khoa-bieu/<int:lop_id>/', views.xem_thoi_khoa_bieu, name='xem_thoi_khoa_bieu'),

    path("profile-hs/", views.hs_profile, name="hs_profile"),
    path("doi-mat-khau-hs/", views.doi_mat_khau, name="hs_doi_mat_khau"),
]
