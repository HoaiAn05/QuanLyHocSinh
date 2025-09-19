# notifications/models.py
from django.db import models

from django.core.mail import send_mail

class ThongBao(models.Model):
    tieu_de = models.CharField(max_length=200)
    noi_dung = models.TextField()
    ngay_gui = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.tieu_de

    def title(self):
        return self.tieu_de
    title.short_description = 'Tiêu đề'

    def created_at(self):
        return self.ngay_gui
    created_at.short_description = 'Ngày tạo'
