# from rest_framework import viewsets
# from .models import GiaoVien
# from .serializers import GiaoVienSerializer
# from rest_framework.permissions import IsAuthenticated
#
# class GiaoVienViewSet(viewsets.ModelViewSet):
#     queryset = GiaoVien.objects.all()
#     serializer_class = GiaoVienSerializer
#     permission_classes = [IsAuthenticated]
#
#
# teachers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.models import User
from teachers.models import GiaoVien
from subjects.models import MonHoc
from accounts.views import is_admin
from django.db.models import Q

# Danh sách giáo viên
@login_required
@user_passes_test(is_admin, login_url="login_page")
def teacher_list(request):
    teachers = GiaoVien.objects.select_related("mon_day")
    q = request.GET.get("q", "")  # lấy từ khóa tìm kiếm

    if q:
        teachers = teachers.filter(
            Q(ho_ten__icontains=q) | Q(mon_day__ten_mon__icontains=q)
        )

    return render(request, "teachers/teacher_list.html", {"teachers": teachers,  "q": q,})

# Thêm giáo viên
@login_required
@user_passes_test(is_admin, login_url="login_page")
def teacher_add(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        ho_ten = request.POST.get("ho_ten")
        email = request.POST.get("email")
        so_dien_thoai = request.POST.get("so_dien_thoai")
        mon_day_id = request.POST.get("mon_day")

        # Kiểm tra trùng username
        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠️ Username đã tồn tại!")
            return redirect("teacher_add")

        # Kiểm tra bắt buộc chọn môn dạy
        if not mon_day_id:
            messages.error(request, "⚠️ Vui lòng chọn môn dạy cho giáo viên!")
            return redirect("teacher_add")

        try:
            mon_day = MonHoc.objects.get(pk=mon_day_id)
        except MonHoc.DoesNotExist:
            messages.error(request, "⚠️ Môn học không tồn tại!")
            return redirect("teacher_add")

        # Tạo tài khoản user
        user = User.objects.create(
            username=username,
            password=make_password(password),
            role="teacher",
        )

        # Tạo giáo viên
        GiaoVien.objects.create(
            user=user,
            ho_ten=ho_ten,
            email=email,
            so_dien_thoai=so_dien_thoai,
            mon_day=mon_day,
        )

        messages.success(request, f"✅ Đã thêm giáo viên {ho_ten}")
        return redirect("teacher_list")

    mon_hoc_list = MonHoc.objects.all()
    return render(request, "teachers/teacher_form.html", {"mon_hoc_list": mon_hoc_list})


# Sửa giáo viên
@login_required
@user_passes_test(is_admin, login_url="login_page")
def teacher_edit(request, pk):
    teacher = get_object_or_404(GiaoVien, pk=pk)

    if request.method == "POST":
        teacher.ho_ten = request.POST.get("ho_ten")
        teacher.email = request.POST.get("email")
        teacher.so_dien_thoai = request.POST.get("so_dien_thoai")
        mon_day_id = request.POST.get("mon_day")

        teacher.mon_day = MonHoc.objects.get(pk=mon_day_id) if mon_day_id else None
        teacher.save()

        messages.success(request, "Cập nhật thông tin giáo viên thành công")
        return redirect("teacher_list")

    mon_hoc_list = MonHoc.objects.all()
    return render(request, "teachers/teacher_form.html", {"teacher": teacher, "mon_hoc_list": mon_hoc_list})

# Xóa giáo viên
@login_required
@user_passes_test(is_admin, login_url="login_page")
def teacher_delete(request, pk):
    teacher = get_object_or_404(GiaoVien, pk=pk)
    teacher.user.delete()
    teacher.delete()
    messages.success(request, "Đã xóa giáo viên")
    return redirect("teacher_list")


from django.contrib.auth import update_session_auth_hash
from .forms import GiaoVienProfileForm, AvatarUploadForm, CustomPasswordChangeForm


@login_required
def giao_vien_profile(request):
    giao_vien = get_object_or_404(GiaoVien, user=request.user)

    if request.method == "POST":
        avatar_form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(request, "Cập nhật avatar thành công!")
            return redirect("giao_vien_profile")
    else:
        avatar_form = AvatarUploadForm(instance=request.user)

    return render(request, "teachers/profile.html", {
        "giao_vien": giao_vien,
        "avatar_form": avatar_form,
    })



@login_required
def doi_mat_khau(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # giữ phiên đăng nhập
            messages.success(request, "Đổi mật khẩu thành công!")
            return redirect("giao_vien_profile")
        else:
            messages.error(request, "Có lỗi khi đổi mật khẩu.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, "teachers/change_password.html", {"form": form})


from classes.models import TietHoc

@login_required
def xem_lich_day(request):
    giao_vien = request.user.giaovien  # giả sử User có OneToOne với GiaoVien
    lich = TietHoc.objects.filter(phan_cong__giao_vien=giao_vien).order_by("thu", "tiet")
    return render(request, "teachers/xem_lich_day.html", {"lich": lich})

