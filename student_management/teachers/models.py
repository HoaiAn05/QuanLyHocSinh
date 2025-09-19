# teachers/models.py
from django.db import models


class GiaoVien(models.Model):
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    ho_ten = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    so_dien_thoai = models.CharField(max_length=20, null=True, blank=True)
    mon_day = models.ForeignKey('subjects.MonHoc', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.ho_ten} "

    # === alias cho admin (full_name, teacher_code, phone)
    def full_name(self):
        return self.ho_ten
    full_name.short_description = 'Họ tên'

    def phone(self):
        return self.so_dien_thoai
    phone.short_description = 'Số điện thoại'

    def mon(self):
        return self.mon_day
    phone.short_description = 'Môn dạy'

