# students/models.py
from datetime import date

from django.db import models


class HocSinh(models.Model):
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    ho_ten = models.CharField(max_length=100)
    ngay_sinh = models.DateField()
    gioi_tinh = models.CharField(
        max_length=10,
        choices=[('Nam', 'Nam'), ('Nu', 'Nữ'), ('Khac', 'Khác')],
        default='Nam'
    )
    lop = models.ForeignKey('classes.LopHoc', on_delete=models.SET_NULL, null=True, blank=True,  related_name='hoc_sinhs')
    email_phu_huynh = models.EmailField(null=True, blank=True)

    class Meta:
        ordering = ['ho_ten']


    @property
    def age(self):
        today = date.today()
        return today.year - self.ngay_sinh.year - (
                (today.month, today.day) < (self.ngay_sinh.month, self.ngay_sinh.day)
        )

    def __str__(self):
        return f"{self.ho_ten}"

    # === alias cho admin (full_name, student_code, dob, gender, classroom)
    def full_name(self):
        return self.ho_ten

    full_name.short_description = 'Họ tên'

    def student_code(self):
        return self.ma_hoc_sinh

    student_code.short_description = 'Mã học sinh'

    def dob(self):
        return self.ngay_sinh

    dob.short_description = 'Ngày sinh'

    def gender(self):
        return self.gioi_tinh

    gender.short_description = 'Giới tính'

    def classroom(self):
        return self.lop

    classroom.short_description = 'Lớp'
