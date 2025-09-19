# monhoc/models.py
from django.db import models

class MonHoc(models.Model):
    ma_mon = models.CharField(max_length=20, unique=True)
    ten_mon = models.CharField(max_length=100)

    def __str__(self):
        return self.ten_mon

    # === alias cho admin (name, code)
    def name(self):
        return self.ten_mon
    name.short_description = 'Ten mon'

    def code(self):
        return self.ma_mon
    code.short_description = 'Ma mon'
