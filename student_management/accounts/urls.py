from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login_page"),
    path("logout/", views.logout_view, name="logout_page"),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("teacher-dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),



]
