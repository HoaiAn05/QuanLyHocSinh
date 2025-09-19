# classes/models.py
from django.db import models



class LopHoc(models.Model):
    name = models.CharField(max_length=50, unique=True)
    giao_vien_chu_nhiem = models.ForeignKey(
        'teachers.GiaoVien',  # dùng string để tránh vòng import
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='lop_chu_nhiems'
    )
    nam_hoc = models.ForeignKey('scores.NamHoc',  on_delete=models.SET_NULL,null=True, blank=True , default=1)

    def si_so(self):
        return self.hoc_sinhs.count()  # lấy từ related_name trong User

    def __str__(self):
        return self.name


class PhanCongGiangDay(models.Model):
    lop = models.ForeignKey("classes.LopHoc", on_delete=models.CASCADE, related_name="phan_congs")
    giao_vien = models.ForeignKey("teachers.GiaoVien", on_delete=models.CASCADE, related_name="phan_congs")
    mon_hoc = models.ForeignKey("subjects.MonHoc", on_delete=models.CASCADE, related_name="phan_congs")
    nam_hoc = models.ForeignKey("scores.NamHoc", on_delete=models.CASCADE,null=True, blank=True, related_name="phan_congs", default=1)

    class Meta:
        unique_together = ("lop", "giao_vien", "mon_hoc", "nam_hoc")  # tránh trùng phân công trong cùng năm

    def __str__(self):
        return f"{self.lop.name} - {self.mon_hoc.ten_mon} ({self.giao_vien.ho_ten}) [{self.nam_hoc}]"


class TietHoc(models.Model):
    phan_cong = models.ForeignKey("classes.PhanCongGiangDay", on_delete=models.CASCADE, related_name="tiet_hoc")
    thu = models.IntegerField(choices=[
        (2, "Thứ 2"),
        (3, "Thứ 3"),
        (4, "Thứ 4"),
        (5, "Thứ 5"),
        (6, "Thứ 6"),
        (7, "Thứ 7"),
    ])
    tiet = models.IntegerField()  # tiết học trong ngày (1, 2, 3,...)

    def __str__(self):
        return f"{self.phan_cong.lop.name} - {self.phan_cong.mon_hoc.ten_mon} (GV: {self.phan_cong.giao_vien.ho_ten})"
