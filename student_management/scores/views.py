from classes.models import PhanCongGiangDay, LopHoc
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from scores.models import NamHoc
from students.models import HocSinh
from subjects.models import MonHoc
from teachers.models import GiaoVien

from .forms import LopNamHocForm
from .models import Diem


@login_required
def chon_lop_nam_hoc(request):
    giao_vien = GiaoVien.objects.get(user=request.user)  # lấy user đang đăng nhập

    if request.method == "POST":
        form = LopNamHocForm(request.POST, giao_vien=giao_vien)
        if form.is_valid():
            lop_id = form.cleaned_data["lop"].id
            nam_hoc_id = form.cleaned_data["nam_hoc"].id
            hoc_ky_id = form.cleaned_data["hoc_ky"].id

            # lưu session để dùng lại
            request.session["lop_id"] = lop_id
            request.session["nam_hoc_id"] = nam_hoc_id
            request.session["hoc_ky_id"] = hoc_ky_id

            if "nhap_diem" in request.POST:
                return redirect("nhap_diem_lop", lop_id=lop_id)
            elif "xem_bang_diem" in request.POST:
                return redirect("xem_bang_diem_lop", lop_id=lop_id)
    else:
        form = LopNamHocForm(giao_vien=giao_vien)

    return render(request, "scores/chon_lop_nam.html", {"form": form})


# @login_required
# def nhap_diem_lop(request, lop_id):
#     lop = get_object_or_404(LopHoc, id=lop_id)
#     hoc_sinh_list = HocSinh.objects.filter(lop=lop)
#
#     nam_hoc_id = request.session.get("nam_hoc_id")
#     hoc_ky_id = request.session.get("hoc_ky_id")
#     giao_vien = get_object_or_404(GiaoVien, user=request.user)
#     mon_hoc = giao_vien.mon_day
#
#     if request.method == "POST":
#         for hs in hoc_sinh_list:
#             for loai_diem in ["mieng", "15p", "gk", "ck"]:
#                 value = request.POST.get(f"{hs.id}_{loai_diem}")
#                 if value:
#                     Diem.objects.create(
#                         hoc_sinh=hs,
#                         mon_hoc_id=mon_hoc,  # giả sử mặc định môn, có thể cho chọn thêm
#                         nam_hoc_id=nam_hoc_id,
#                         hoc_ky_id=hoc_ky_id,
#                         loai_diem=loai_diem,
#                         diem=float(value)
#                     )
#         return redirect("xem_bang_diem_lop", lop_id=lop_id)
#
#     return render(request, "scores/nhap_diem.html", {
#         "lop": lop,
#         "hoc_sinh_list": hoc_sinh_list,
#         "mon_hoc": mon_hoc,
#
#     })

@login_required
def nhap_diem_lop(request, lop_id):
    lop = get_object_or_404(LopHoc, id=lop_id)
    hoc_sinh_list = HocSinh.objects.filter(lop=lop).order_by("ho_ten")

    nam_hoc_id = request.session.get("nam_hoc_id")
    hoc_ky_id = request.session.get("hoc_ky_id")

    giao_vien = get_object_or_404(GiaoVien, user=request.user)
    mon_hoc = giao_vien.mon_day

    if request.method == "POST":
        for hs in hoc_sinh_list:
            # Lấy danh sách điểm miệng (nhiều input => list)
            diem_mieng_list = request.POST.getlist(f"diem_mieng_{hs.id}[]")

            # Các điểm khác (chỉ 1 giá trị)
            diem_15p = request.POST.get(f"diem_15p_{hs.id}")
            diem_1tiet = request.POST.get(f"diem_1tiet_{hs.id}")
            diem_cuoiky = request.POST.get(f"diem_cuoiky_{hs.id}")

            # Lưu từng điểm miệng
            for diem in diem_mieng_list:
                if diem.strip():
                    Diem.objects.create(
                        hoc_sinh=hs,
                        mon_hoc=mon_hoc,
                        nam_hoc_id=nam_hoc_id,
                        hoc_ky_id=hoc_ky_id,
                        loai_diem="mieng",
                        diem_so=float(diem)
                    )

            # Lưu điểm 15p
            if diem_15p:
                Diem.objects.update_or_create(
                    hoc_sinh=hs,
                    mon_hoc=mon_hoc,
                    nam_hoc_id=nam_hoc_id,
                    hoc_ky_id=hoc_ky_id,
                    loai_diem="15p",
                    defaults={"diem_so": float(diem_15p)},
                )

            # Lưu điểm 1 tiết
            if diem_1tiet:
                Diem.objects.update_or_create(
                    hoc_sinh=hs,
                    mon_hoc=mon_hoc,
                    nam_hoc_id=nam_hoc_id,
                    hoc_ky_id=hoc_ky_id,
                    loai_diem="gk",
                    defaults={"diem_so": float(diem_1tiet)},
                )

            # Lưu điểm cuối kỳ
            if diem_cuoiky:
                Diem.objects.update_or_create(
                    hoc_sinh=hs,
                    mon_hoc=mon_hoc,
                    nam_hoc_id=nam_hoc_id,
                    hoc_ky_id=hoc_ky_id,
                    loai_diem="ck",
                    defaults={"diem_so": float(diem_cuoiky)},
                )

        return redirect("xem_bang_diem_lop", lop_id=lop.id)

    return render(request, "scores/nhap_diem.html", {
        "lop": lop,
        "hoc_sinh_list": hoc_sinh_list,
        "mon_hoc": mon_hoc,
        "nam_hoc_id": nam_hoc_id,
        "hoc_ky_id": hoc_ky_id,
    })


@login_required
def xem_bang_diem_lop(request, lop_id):
    lop = get_object_or_404(LopHoc, id=lop_id)
    giao_vien = get_object_or_404(GiaoVien, user=request.user)  # giáo viên đăng nhập

    # Lấy năm học và học kỳ từ session
    nam_hoc_id = request.session.get("nam_hoc_id")
    hoc_ky_id = request.session.get("hoc_ky_id")

    # Tìm môn mà giáo viên này dạy ở lớp đó

    phan_cong = PhanCongGiangDay.objects.get(
        lop=lop, giao_vien=giao_vien, nam_hoc_id=nam_hoc_id
    )

    mon_hoc = phan_cong.mon_hoc


    hoc_sinh_list = HocSinh.objects.filter(lop=lop)
    bang_diem = []

    for hs in hoc_sinh_list:
        diem_list = Diem.objects.filter(
            hoc_sinh=hs,
            mon_hoc=mon_hoc,  #  chỉ lọc điểm môn giáo viên dạy
            nam_hoc_id=nam_hoc_id,
            hoc_ky_id=hoc_ky_id
        )

        diem_mieng = list(diem_list.filter(loai_diem="mieng").values_list("diem_so", flat=True))
        diem_15p = list(diem_list.filter(loai_diem="15p").values_list("diem_so", flat=True))
        diem_gk = list(diem_list.filter(loai_diem="gk").values_list("diem_so", flat=True))
        diem_ck = list(diem_list.filter(loai_diem="ck").values_list("diem_so", flat=True))

        # Tính trung bình có trọng số
        tong, hs_weight = 0, 0
        for d in diem_mieng: tong += d; hs_weight += 1
        for d in diem_15p: tong += d; hs_weight += 1
        for d in diem_gk: tong += d * 2; hs_weight += 2
        for d in diem_ck: tong += d * 3; hs_weight += 3
        tb = round(tong / hs_weight, 2) if hs_weight > 0 else None

        bang_diem.append({
            "hoc_sinh": hs,
            "diem_mieng": diem_mieng,
            "diem_15p": diem_15p,
            "diem_gk": diem_gk,
            "diem_ck": diem_ck,
            "tb": tb,
        })

    return render(request, "scores/xem_bang_diem.html", {
        "lop": lop,
        "mon_hoc": mon_hoc,  # để hiện tên môn trên template
        "bang_diem": bang_diem,
    })


@login_required
def chon_hoc_ky_hs(request):
    if request.method == "POST":
        nam_hoc_id = request.POST.get("nam_hoc")
        hoc_ky_id = request.POST.get("hoc_ky")

        request.session["nam_hoc_id"] = int(nam_hoc_id)
        request.session["hoc_ky_id"] = int(hoc_ky_id)

        return redirect("xem_bang_diem_hoc_sinh")  # hoặc dashboard học sinh

    nam_hoc_list = NamHoc.objects.all()
    return render(request, "scores/chon_hoc_ky_hs.html", {
        "nam_hoc_list": nam_hoc_list
    })


@login_required
def xem_bang_diem_hoc_sinh(request):
    hoc_sinh = get_object_or_404(HocSinh, user=request.user)

    nam_hoc_id = request.session.get("nam_hoc_id")
    hoc_ky_id = request.session.get("hoc_ky_id")

    if not nam_hoc_id or not hoc_ky_id:
        return redirect("chon_hoc_ky_hs")

    mon_list = MonHoc.objects.all()
    bang_diem = []

    tong_tb = 0
    tong_mon = 0

    for mon in mon_list:
        diem_list = Diem.objects.filter(
            hoc_sinh=hoc_sinh,
            mon_hoc=mon,
            nam_hoc_id=nam_hoc_id,
            hoc_ky_id=hoc_ky_id
        )

        diem_mieng = list(diem_list.filter(loai_diem="mieng").values_list("diem_so", flat=True))
        diem_15p = list(diem_list.filter(loai_diem="15p").values_list("diem_so", flat=True))
        diem_gk = list(diem_list.filter(loai_diem="gk").values_list("diem_so", flat=True))
        diem_ck = list(diem_list.filter(loai_diem="ck").values_list("diem_so", flat=True))

        # Tính trung bình môn
        tong, hs_weight = 0, 0
        for d in diem_mieng: tong += d; hs_weight += 1
        for d in diem_15p: tong += d; hs_weight += 1
        for d in diem_gk: tong += d * 2; hs_weight += 2
        for d in diem_ck: tong += d * 3; hs_weight += 3
        tb_mon = round(tong / hs_weight, 2) if hs_weight > 0 else None

        # Nếu có điểm thì tính vào tổng kết
        if tb_mon is not None:
            tong_tb += tb_mon
            tong_mon += 1

        bang_diem.append({
            "mon": mon.ten_mon,
            "diem_mieng": diem_mieng,
            "diem_15p": diem_15p,
            "diem_gk": diem_gk,
            "diem_ck": diem_ck,
            "tb_mon": tb_mon,
        })

    # Điểm tổng kết học kỳ
    tb_hoc_ky = round(tong_tb / tong_mon, 2) if tong_mon > 0 else None

    # Nếu là học kỳ 2 → tính điểm cả năm
    tb_ca_nam = None
    if int(hoc_ky_id) == 2:
        tong_tb_nam = 0
        tong_mon_nam = 0
        for mon in mon_list:
            diem_hk1 = Diem.objects.filter(hoc_sinh=hoc_sinh, mon_hoc=mon, nam_hoc_id=nam_hoc_id, hoc_ky_id=1)
            diem_hk2 = Diem.objects.filter(hoc_sinh=hoc_sinh, mon_hoc=mon, nam_hoc_id=nam_hoc_id, hoc_ky_id=2)

            def tinh_tb(diem_list):
                tong, hs_weight = 0, 0
                diem_mieng = list(diem_list.filter(loai_diem="mieng").values_list("diem_so", flat=True))
                diem_15p = list(diem_list.filter(loai_diem="15p").values_list("diem_so", flat=True))
                diem_gk = list(diem_list.filter(loai_diem="gk").values_list("diem_so", flat=True))
                diem_ck = list(diem_list.filter(loai_diem="ck").values_list("diem_so", flat=True))
                for d in diem_mieng: tong += d; hs_weight += 1
                for d in diem_15p: tong += d; hs_weight += 1
                for d in diem_gk: tong += d * 2; hs_weight += 2
                for d in diem_ck: tong += d * 3; hs_weight += 3
                return round(tong / hs_weight, 2) if hs_weight > 0 else None

            tb1 = tinh_tb(diem_hk1)
            tb2 = tinh_tb(diem_hk2)

            if tb1 is not None or tb2 is not None:
                if tb1 is None: tb1 = 0
                if tb2 is None: tb2 = 0
                tb_nam_mon = round((tb1 + tb2 * 2) / 3, 2)  # hk2 hệ số 2
                tong_tb_nam += tb_nam_mon
                tong_mon_nam += 1

        tb_ca_nam = round(tong_tb_nam / tong_mon_nam, 2) if tong_mon_nam > 0 else None

    return render(request, "scores/xem_bang_diem_hs.html", {
        "hoc_sinh": hoc_sinh,
        "bang_diem": bang_diem,
        "tb_hoc_ky": tb_hoc_ky,
        "tb_ca_nam": tb_ca_nam,
        "hoc_ky_id": hoc_ky_id,
    })

#============================================================


def bao_cao_diem(request):
    nam_id = request.GET.get("nam")
    mon_id = request.GET.get("mon")
    lop_id = request.GET.get("lop")

    nam_hoc = NamHoc.objects.get(id=nam_id) if nam_id else None
    mon_hoc = MonHoc.objects.get(id=mon_id) if mon_id else None
    lop_hoc = LopHoc.objects.get(id=lop_id) if lop_id else None

    labels, data = [], []
    tong = dat = khongdat = 0

    if nam_hoc and mon_hoc:
        # --- Báo cáo theo môn ---
        for hs in HocSinh.objects.all():
            tb = Diem.tinh_trung_binh_ca_nam(hs, mon_hoc, nam_hoc)
            if tb is not None:
                tong += 1
                if tb >= 5:
                    dat += 1
                else:
                    khongdat += 1
        labels = ["Đạt (>=5)", "Không đạt (<5)"]
        data = [dat, khongdat]

    elif nam_hoc and lop_hoc:
        # --- Báo cáo theo lớp ---
        for hs in HocSinh.objects.filter(lop=lop_hoc):
            tong_m = 0
            dem_m = 0
            for m in MonHoc.objects.all():
                tb = Diem.tinh_trung_binh_ca_nam(hs, m, nam_hoc)
                if tb is not None:
                    tong_m += tb
                    dem_m += 1
            if dem_m > 0:
                tb_cn = round(tong_m / dem_m, 2)
                tong += 1
                if tb_cn >= 5:
                    dat += 1
                else:
                    khongdat += 1
        labels = ["Đạt (>=5)", "Không đạt (<5)"]
        data = [dat, khongdat]

    ti_le_dat = round(dat / tong * 100, 2) if tong > 0 else 0
    ti_le_khongdat = round(khongdat / tong * 100, 2) if tong > 0 else 0

    return render(request, "scores/bao_cao_diem.html", {
        "labels": labels,
        "data": data,
        "nam_hoc": nam_hoc,
        "mon_hoc": mon_hoc,
        "lop_hoc": lop_hoc,
        "tong": tong,
        "dat": dat,
        "khongdat": khongdat,
        "ti_le_dat": ti_le_dat,
        "ti_le_khongdat": ti_le_khongdat,
        "nam_list": NamHoc.objects.all(),
        "mon_list": MonHoc.objects.all(),
        "lop_list": LopHoc.objects.all(),
    })


