# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from accounts.views import is_admin
from .models import HocSinh
from .forms import HocSinhForm, ClassroomAssignForm
from classes.models import LopHoc

User = get_user_model()
def generate_unique_username(full_name):
    """
    Tạo username duy nhất từ họ tên học sinh
    """
    base_username = slugify(full_name.replace("đ", "d").replace("Đ", "D"))
    if not base_username:
        base_username = "student"

    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username


@login_required
@user_passes_test(is_admin, login_url="login_page")
def student_list(request):
    students = HocSinh.objects.select_related("lop").filter(lop__isnull=True)
    return render(request, "students/student_list.html", {"students": students})


@login_required
@user_passes_test(is_admin, login_url="login_page")
def student_add(request):
    if request.method == "POST":
        form = HocSinhForm(request.POST)
        if form.is_valid():
            hoc_sinh = form.save(commit=False)

            # 🔹 Kiểm tra tuổi
            if not (15 <= hoc_sinh.age <= 20):
                messages.error(
                    request,
                    f"Học sinh {hoc_sinh.ho_ten} ({hoc_sinh.age} tuổi) không thuộc độ tuổi 15–20."
                )
                return render(request, 'students/student_form.html', {'form': form})

            classroom: LopHoc = hoc_sinh.lop
            # 🔹 Nếu học sinh có chọn lớp thì kiểm tra sĩ số
            if classroom and classroom.hoc_sinhs.count() >= 40:
                messages.error(request, f"Lớp {classroom.name} đã đủ sĩ số (40).")
                return render(request, 'students/student_form.html', {'form': form})

            # 🔹 Tạo username từ họ tên (tránh trùng lặp)
            base_username = hoc_sinh.ho_ten.lower().replace(" ", "")
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # 🔹 Tạo user cho học sinh
            user = User.objects.create_user(
                username=username,
                password="123"  # mật khẩu mặc định
            )
            hoc_sinh.user = user
            hoc_sinh.save()

            messages.success(request, f"Thêm học sinh {hoc_sinh.ho_ten} thành công!")
            return redirect("student_list")
    else:
        form = HocSinhForm()
    return render(request, 'students/student_form.html', {'form': form})



@login_required
@user_passes_test(is_admin, login_url="login_page")
def student_edit(request, pk):
    student = get_object_or_404(HocSinh, pk=pk)
    if request.method == "POST":
        form = HocSinhForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật học sinh thành công")
            return redirect("student_list")
    else:
        form = HocSinhForm(instance=student)
    return render(request, "students/student_form.html", {"form": form})


@login_required
@user_passes_test(is_admin, login_url="login_page")
def student_delete(request, pk):
    student = get_object_or_404(HocSinh, pk=pk)
    if student.user:  # xóa luôn user đi kèm
        student.user.delete()
    student.delete()
    messages.success(request, "Xóa học sinh thành công")
    return redirect("student_list")


@login_required
@user_passes_test(is_admin, login_url="login_page")
def assign_classroom(request, pk):
    student = get_object_or_404(HocSinh, pk=pk)

    if request.method == "POST":
        form = ClassroomAssignForm(student, request.POST)
        if form.is_valid():
            # 🔹 Kiểm tra tuổi
            if not (15 <= student.age <= 20):
                messages.error(
                    request,
                    f"Học sinh {student.ho_ten} ({student.age} tuổi) không thuộc độ tuổi 15–20, không thể phân lớp."
                )
                return redirect("student_list")

            classroom: LopHoc = form.cleaned_data.get("classroom")

            # 🔹 Nếu classroom None → báo lỗi
            if classroom is None:
                messages.error(request, "Bạn chưa chọn lớp học.")
                return redirect("student_list")

            # 🔹 Kiểm tra sĩ số lớp
            if classroom.hoc_sinhs.count() >= 40:
                messages.error(request, "Lớp đã đủ sĩ số (40).")
                return redirect("student_list")

            # 🔹 Gán lớp cho học sinh
            student.lop = classroom
            student.save()
            messages.success(request, f"Đã phân {student.ho_ten} vào lớp {classroom.name}")
            return redirect("student_list")
        else:
            # 🔹 Nếu form không hợp lệ → báo lỗi
            messages.error(request, f"Lỗi form: {form.errors}")
            return redirect("student_list")
    else:
        form = ClassroomAssignForm(student)

    return render(request, "students/assign_classroom.html", {"form": form, "student": student})



from classes.models import TietHoc

@login_required
def xem_thoi_khoa_bieu(request, lop_id):
    lop = get_object_or_404(LopHoc, id=lop_id)
    hoc_sinh = request.user.hocsinh  # giả sử User có OneToOne với HocSinh
    tkb = TietHoc.objects.filter(phan_cong__lop=hoc_sinh.lop).order_by("thu", "tiet")
    return render(request, "students/xem_thoi_khoa_bieu.html", {"tkb": tkb, "lop": lop,} )

from classes.forms import TietHocForm

def tkb_list(request):
    tkb = (
        TietHoc.objects.select_related(
            "phan_cong__lop", "phan_cong__mon_hoc", "phan_cong__giao_vien"
        )
        .order_by("phan_cong__lop__name", "thu", "tiet")
    )
    return render(request, "students/list_tkb.html", {"tkb": tkb})


def tkb_create(request):
    if request.method == "POST":
        form = TietHocForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tkb_list")
    else:
        form = TietHocForm()
    return render(request, "students/tkb_form.html", {"form": form})

def tkb_update(request, pk):
    tiet = get_object_or_404(TietHoc, pk=pk)
    if request.method == "POST":
        form = TietHocForm(request.POST, instance=tiet)
        if form.is_valid():
            form.save()
            return redirect("tkb_list")
    else:
        form = TietHocForm(instance=tiet)
    return render(request, "students/tkb_form.html", {"form": form})

def tkb_delete(request, pk):
    tiet = get_object_or_404(TietHoc, pk=pk)
    if request.method == "POST":
        tiet.delete()
        return redirect("tkb_list")
    return render(
        request,
        "students/tkb_form.html",
        {"tiet": tiet, "delete": True},
    )



from django.contrib.auth import update_session_auth_hash
from .forms import HSProfileForm, HSAvatarUploadForm, CustomPasswordChangeForm


@login_required
def hs_profile(request):
    hoc_sinh = get_object_or_404(HocSinh, user=request.user)

    if request.method == "POST":
        avatar_form = HSAvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if avatar_form.is_valid():
            avatar_form.save()
            messages.success(request, "Cập nhật avatar thành công!")
            return redirect("hs_profile")
    else:
        avatar_form = HSAvatarUploadForm(instance=request.user)

    return render(request, "students/profile_hs.html", {
        "hoc_sinh": hoc_sinh,
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
            return redirect("hs_profile")
        else:
            messages.error(request, "Có lỗi khi đổi mật khẩu.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, "students/doi_mat_khau.html", {"form": form})


