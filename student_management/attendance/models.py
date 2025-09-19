
from django.db import models

class DiemDanh(models.Model):
    TRANG_THAI_CHOICES = [
        ('C', 'Có mặt'),
        ('V',   'Vắng'),
        ('M',    'Trễ'),
    ]
    hoc_sinh = models.ForeignKey('students.HocSinh', on_delete=models.CASCADE)
    ngay = models.DateField()
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI_CHOICES, default='C')

    class Meta:
        unique_together = ('hoc_sinh', 'ngay')

    def __str__(self):
        return f"{self.hoc_sinh} - {self.ngay} - {self.trang_thai}"

    # === alias cho admin (student, date, status)
    def student(self):
        return self.hoc_sinh
    student.short_description = 'Hoc sinh'

    def date(self):
        return self.ngay
    date.short_description = 'Ngay'

    def status(self):
        return self.get_trang_thai_display()
    status.short_description = 'Trang thai'
