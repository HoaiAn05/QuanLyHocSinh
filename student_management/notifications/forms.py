from django import forms
from .models import ThongBao

class ThongBaoForm(forms.ModelForm):
    class Meta:
        model = ThongBao
        fields = ['tieu_de', 'noi_dung']
        labels = {
            "tieu_de": "Tiêu đề",
            "noi_dung": "Nội dung",
        }
        widgets = {
            'tieu_de': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề thông báo'
            }),
            'noi_dung': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Nhập nội dung thông báo...'
            }),
        }
