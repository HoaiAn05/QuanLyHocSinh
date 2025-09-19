
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class NamHoc(models.Model):
    ten_nam = models.CharField(max_length=20, unique=True)  # ví dụ: 2024-2025

    def __str__(self):
        return self.ten_nam


class HocKy(models.Model):
    HOC_KY_CHOICES = (
        (1, "Học kỳ 1"),
        (2, "Học kỳ 2"),
    )
    ten_hoc_ky = models.IntegerField(choices=HOC_KY_CHOICES)

    def __str__(self):
        return f"Học kỳ {self.ten_hoc_ky}"


class Diem(models.Model):
    LOAI_DIEM_CHOICES = (
        ("mieng", "Điểm miệng"),
        ("15p", "Điểm 15 phút"),
        ("gk", "Giữa kỳ"),
        ("ck", "Cuối kỳ"),
    )

    hoc_sinh = models.ForeignKey(
        "students.HocSinh",
        on_delete=models.CASCADE,
        related_name="ds_diem"
    )
    mon_hoc = models.ForeignKey(
        "subjects.MonHoc",
        on_delete=models.CASCADE,
        related_name="ds_diem"
    )
    nam_hoc = models.ForeignKey(
        "scores.NamHoc",
        on_delete=models.CASCADE,
        related_name="ds_diem"
    )
    hoc_ky = models.ForeignKey(
        "scores.HocKy",
        on_delete=models.CASCADE,
        related_name="ds_diem"
    )

    loai_diem = models.CharField(max_length=10, choices=LOAI_DIEM_CHOICES)
    diem_so = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    ngay_nhap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hoc_sinh} - {self.mon_hoc} ({self.loai_diem}: {self.diem_so})"


    # Tính trung bình cho 1 học sinh / môn / học kỳ
    @staticmethod
    def tinh_trung_binh(hoc_sinh, mon_hoc, nam_hoc, hoc_ky):
        qs = Diem.objects.filter(
            hoc_sinh=hoc_sinh,
            mon_hoc=mon_hoc,
            nam_hoc=nam_hoc,
            hoc_ky=hoc_ky,
        )

        # nhóm điểm
        diem_mieng = [d.diem_so for d in qs.filter(loai_diem="mieng")]
        diem_15p   = [d.diem_so for d in qs.filter(loai_diem="15p")]
        diem_gk    = [d.diem_so for d in qs.filter(loai_diem="gk")]
        diem_ck    = [d.diem_so for d in qs.filter(loai_diem="ck")]

        tong = 0
        he_so = 0

        # hệ số 1
        for d in diem_mieng + diem_15p:
            tong += d * 1
            he_so += 1

        # giữa kỳ hệ số 2
        for d in diem_gk:
            tong += d * 2
            he_so += 2

        # cuối kỳ hệ số 3
        for d in diem_ck:
            tong += d * 3
            he_so += 3

        return round(tong / he_so, 2) if he_so > 0 else None


    #  Tính trung bình cả năm
    @staticmethod
    def tinh_trung_binh_ca_nam(hoc_sinh, mon_hoc, nam_hoc):
        tb_hk1 = Diem.tinh_trung_binh(hoc_sinh, mon_hoc, nam_hoc, hoc_ky=1)
        tb_hk2 = Diem.tinh_trung_binh(hoc_sinh, mon_hoc, nam_hoc, hoc_ky=2)

        if tb_hk1 is None and tb_hk2 is None:
            return None
        if tb_hk1 is None:
            return tb_hk2
        if tb_hk2 is None:
            return tb_hk1

        return round((tb_hk1 + tb_hk2 * 2) / 3, 2)
