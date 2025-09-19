from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import DiemDanh
from .forms import DiemDanhForm
from notifications.models import ThongBao
from django.core.mail import send_mail
from django.conf import settings
from teachers.models import GiaoVien
from classes.models import LopHoc


@login_required
def them_diem_danh(request):
    user = request.user
    giao_vien = getattr(user, "giaovien", None) if user.role == "teacher" else None

    if request.method == "POST":
        form = DiemDanhForm(request.POST, giao_vien=giao_vien)
        if form.is_valid():
            record = form.save()

            # Nếu học sinh vắng thì gửi mail
            if record.trang_thai == 'V' and record.hoc_sinh.email_phu_huynh:
                subject = f"Thông báo vắng học: {record.hoc_sinh.ho_ten}"
                message = f"Học sinh {record.hoc_sinh.ho_ten} đã vắng học ngày {record.ngay}."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [record.hoc_sinh.email_phu_huynh])

                ThongBao.objects.create(tieu_de=subject, noi_dung=message)

            return redirect("danh_sach_diem_danh")
    else:
        form = DiemDanhForm(giao_vien=giao_vien)

    return render(request, "attendance/them_diem_danh.html", {"form": form})


@login_required
def danh_sach_diem_danh(request):
    user = request.user
    giao_vien = getattr(user, "giaovien", None)

    if user.role == "teacher" and giao_vien:
        # Chỉ lấy học sinh thuộc lớp mà GV này làm chủ nhiệm
        lop_ids = LopHoc.objects.filter(giao_vien_chu_nhiem=giao_vien).values_list("id", flat=True)
        records = DiemDanh.objects.filter(hoc_sinh__lop_id__in=lop_ids)
    else:
        # Admin xem tất cả
        records = DiemDanh.objects.all()

    return render(request, "attendance/danh_sach_diem_danh.html", {"records": records})
