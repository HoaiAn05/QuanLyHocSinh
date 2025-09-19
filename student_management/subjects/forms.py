from django import forms
from .models import MonHoc


class MonHocForm(forms.ModelForm):
    class Meta:
        model = MonHoc
        fields = ['ma_mon', 'ten_mon']
        labels = {
            "ma_mon": "Mã môn",
            "ten_mon": "Tên môn"
        }