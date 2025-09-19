#accounts.views
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def home(request):
    return render(request, "accounts/home.html")

# ===============================
# Helpers kiểm tra role
# ===============================
def is_admin(user):
    return user.is_authenticated and user.is_superuser

def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'teacher'

def is_student(user):
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'student'

# ===============================
# Login / Logout
# ===============================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Điều hướng theo role
            if user.is_superuser:
                return redirect("admin_dashboard")
            elif hasattr(user, 'role') and user.role == "teacher":
                return redirect("teacher_dashboard")
            elif hasattr(user, 'role') and user.role == "student":
                return redirect("student_dashboard")
            else:
                messages.error(request, "Tài khoản không có quyền truy cập.")
                return redirect("login_page")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng." )
            return redirect("login_page")

    return render(request, "accounts/login.html")


@login_required(login_url="login_page")
def logout_view(request):
    logout(request)
    return redirect("login_page")

# ===============================
# Dashboards
# ===============================

# Admin
@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="login_page")
def admin_dashboard(request):
    return render(request, "accounts/admin_dashboard.html")

# Teacher
@login_required(login_url="login_page")
@user_passes_test(is_teacher, login_url="login_page")
def teacher_dashboard(request):
    return render(request, "accounts/teacher_dashboard.html")


#========================
from django.shortcuts import render, redirect, get_object_or_404
from students.models import HocSinh
# Student
@login_required(login_url="login_page")
@user_passes_test(is_student, login_url="login_page")
def student_dashboard(request):
    hoc_sinh = get_object_or_404(HocSinh, user=request.user)
    lop_id = hoc_sinh.lop.id  # lấy lop_id

    return render(request, "accounts/student_dashboard.html", {
        "lop_id": lop_id,
        "hoc_sinh": hoc_sinh,
    })





