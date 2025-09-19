# from rest_framework import viewsets
# from .models import LopHoc
# from .serializers import LopHocSerializer
# from rest_framework.permissions import IsAuthenticated
#
# class LopHocViewSet(viewsets.ModelViewSet):
#     queryset = LopHoc.objects.all()
#     serializer_class = LopHocSerializer
#     permission_classes = [IsAuthenticated]
#

# classes/views.py
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.views import is_admin
from students.models import HocSinh
from .models import LopHoc
from .forms import LopHocForm
from students.forms import HocSinhForm

def _age_from_dob(dob):
    """Tính tuổi từ ngày sinh"""
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@login_required
@user_passes_test(is_admin, login_url="login_page")
def lop_list(request):
    lops = LopHoc.objects.all()
    return render(request, "classes/lop_list.html", {"lops": lops})


@login_required
@user_passes_test(is_admin, login_url="login_page")
def lop_create(request):
    if request.method == "POST":
        form = LopHocForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm lớp học thành công!")
            return redirect("lop_list")
    else:
        form = LopHocForm()
    return render(request, "classes/lop_form.html", {"form": form, "title": "Thêm Lớp học"})


@login_required
@user_passes_test(is_admin, login_url="login_page")
def lop_update(request, pk):
    lop = get_object_or_404(LopHoc, pk=pk)
    if request.method == "POST":
        form = LopHocForm(request.POST, instance=lop)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật lớp học thành công!")
            return redirect("lop_list")
    else:
        form = LopHocForm(instance=lop)
    return render(request, "classes/lop_form.html", {"form": form, "title": "Sửa Lớp học"})


@login_required
@user_passes_test(is_admin, login_url="login_page")
def lop_delete(request, pk):
    lop = get_object_or_404(LopHoc, pk=pk)
    if request.method == "POST":
        lop.delete()
        messages.success(request, "Xóa lớp học thành công!")
        return redirect("lop_list")
    return render(request, "classes/lop_confirm_delete.html", {"lop": lop})


# ============= CHI TIẾT LỚP HỌC & CRUD HỌC SINH TRONG LỚP =============
@login_required
@user_passes_test(is_admin, login_url="login_page")
def lop_detail(request, pk):
    lop = get_object_or_404(LopHoc, pk=pk)
    students = HocSinh.objects.filter(lop=lop)               # HS trong lớp
    free_students = HocSinh.objects.filter(lop__isnull=True) # HS chưa có lớp

    # Form thêm học sinh mới vào DB (tạo HS luôn trong lớp)
    if request.method == "POST" and "create_student" in request.POST:
        form = HocSinhForm(request.POST)
        if form.is_valid():
            hs = form.save(commit=False)
            hs.lop = lop
            # Kiểm tra tuổi
            age = _age_from_dob(hs.ngay_sinh)
            if age is None or not (15 <= age <= 20):
                messages.error(request, "Học sinh phải từ 15–20 tuổi.")
            elif lop.hoc_sinhs.count() >= 40:
                messages.error(request, "Lớp đã đủ sĩ số (40).")
            else:
                hs.save()
                messages.success(request, f"Đã thêm học sinh {hs.ho_ten} vào lớp {lop.name}.")
                return redirect("lop_detail", pk=pk)
    else:
        form = HocSinhForm()

    return render(request, "classes/lop_detail.html", {
        "lop": lop,
        "students": students,
        "free_students": free_students,
        "form": form
    })


# Thêm học sinh đã tồn tại vào lớp
@login_required
@user_passes_test(is_admin, login_url="login_page")
def add_student_to_class(request, pk):
    lop = get_object_or_404(LopHoc, pk=pk)
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        student = get_object_or_404(HocSinh, pk=student_id)

        age = _age_from_dob(student.ngay_sinh)
        if age is None or not (15 <= age <= 20):
            messages.error(request, "Học sinh phải từ 15–20 tuổi.")
        elif lop.hoc_sinhs.count() >= 40:
            messages.error(request, "Lớp đã đủ sĩ số (40).")
        else:
            student.lop = lop
            student.save()
            messages.success(request, f"Đã thêm {student.ho_ten} vào lớp {lop.name}.")
    return redirect("lop_detail", pk=pk)


# Xóa học sinh khỏi lớp
@login_required
@user_passes_test(is_admin, login_url="login_page")
def remove_student_from_class(request, pk, student_id):
    lop = get_object_or_404(LopHoc, pk=pk)
    student = get_object_or_404(HocSinh, pk=student_id)
    student.lop = None
    student.save()
    messages.success(request, f"Đã xóa {student.ho_ten} khỏi lớp {lop.name}.")
    return redirect("lop_detail", pk=pk)


# Cập nhật thông tin học sinh trong lớp
@login_required
@user_passes_test(is_admin, login_url="login_page")
def student_update(request, pk, student_id):
    student = get_object_or_404(HocSinh, pk=student_id)
    lop = get_object_or_404(LopHoc, pk=pk)
    if request.method == "POST":
        form = HocSinhForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật học sinh thành công!")
            return redirect("lop_detail", pk=pk)
    else:
        form = HocSinhForm(instance=student)
    return render(request, "classes/student_form.html", {"form": form, "lop": lop})


# Xóa học sinh khỏi DB (không chỉ khỏi lớp)
@login_required
@user_passes_test(is_admin, login_url="login_page")
def student_delete(request, pk, student_id):
    student = get_object_or_404(HocSinh, pk=student_id)
    lop = get_object_or_404(LopHoc, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Xóa học sinh thành công!")
        return redirect("lop_detail", pk=pk)
    return render(request, "classes/student_confirm_delete.html", {"student": student, "lop": lop})


#========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from classes.models import PhanCongGiangDay
from classes.forms import PhanCongForm
from accounts.views import is_admin
from classes.models import LopHoc
from teachers.models import GiaoVien
from scores.models import NamHoc

@login_required
@user_passes_test(is_admin, login_url="login_page")
def phancong_list(request):
    phancongs = PhanCongGiangDay.objects.select_related("lop", "giao_vien", "mon_hoc", "nam_hoc")
    return render(request, "teachers/phancong_list.html", {"phancongs": phancongs})

@login_required
@user_passes_test(is_admin, login_url="login_page")
def phancong_add(request):
    if request.method == "POST":
        lop_id = request.POST.get("lop")
        giao_vien_id = request.POST.get("giao_vien")
        nam_hoc_id = request.POST.get("nam_hoc")

        giao_vien = GiaoVien.objects.get(pk=giao_vien_id)
        mon_hoc = giao_vien.mon_day  # môn dạy cố định từ giáo viên

        # Kiểm tra phân công trùng (thêm cả năm học vào điều kiện)
        if PhanCongGiangDay.objects.filter(
            lop_id=lop_id, giao_vien_id=giao_vien_id, mon_hoc=mon_hoc, nam_hoc_id=nam_hoc_id
        ).exists():
            messages.error(request, "Phân công này đã tồn tại trong năm học này!")
            return redirect("phancong_add")

        PhanCongGiangDay.objects.create(
            lop_id=lop_id,
            giao_vien_id=giao_vien_id,
            mon_hoc=mon_hoc,
            nam_hoc_id=nam_hoc_id
        )
        messages.success(request, "Thêm phân công thành công!")
        return redirect("phancong_list")

    lops = LopHoc.objects.all()
    giao_viens = GiaoVien.objects.all()
    nam_hocs = NamHoc.objects.all()
    return render(request, "teachers/phancong_form.html", {
        "lops": lops,
        "giao_viens": giao_viens,
        "nam_hocs": nam_hocs
    })



@login_required
@user_passes_test(is_admin, login_url="login_page")
def phancong_edit(request, pk):
    phancong = get_object_or_404(PhanCongGiangDay, pk=pk)
    if request.method == "POST":
        form = PhanCongForm(request.POST, instance=phancong)
        if form.is_valid():
            phancong = form.save(commit=False)
            # Cập nhật lại năm học theo lớp (tránh bị chỉnh sai)
            phancong.nam_hoc = phancong.lop.nam_hoc
            phancong.save()
            messages.success(request, "Cập nhật phân công thành công.")
            return redirect("phancong_list")
    else:
        form = PhanCongForm(instance=phancong)
    return render(request, "teachers/phancong_form.html", {"form": form})

@login_required
@user_passes_test(is_admin, login_url="login_page")
def phancong_delete(request, pk):
    phancong = get_object_or_404(PhanCongGiangDay, pk=pk)
    if request.method == "POST":
        phancong.delete()
        messages.success(request, "Xóa phân công thành công.")
        return redirect("phancong_list")
    return render(request, "teachers/phancong_confirm_delete.html", {"phancong": phancong})
