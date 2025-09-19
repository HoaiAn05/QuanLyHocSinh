from django import forms
from .models import HocSinh
from classes.models import LopHoc
from accounts.models import User
from django.contrib.auth.forms import PasswordChangeForm


class HocSinhForm(forms.ModelForm):
    class Meta:
        model = HocSinh
        fields = ["ho_ten", "ngay_sinh", "gioi_tinh", "lop", "email_phu_huynh"]
        labels = {
            "ho_ten": "Họ tên",
            "ngay_sinh": "Ngày sinh",
            "gioi_tinh": "Giới tính",
            "lop": "Lớp",
            "email_phu_huynh": "Email phụ huynh",
        }
        widgets = {
            "ho_ten": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nhập họ tên"}),
            "ngay_sinh": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "gioi_tinh": forms.Select(attrs={"class": "form-select"}),
            "lop": forms.Select(attrs={"class": "form-select"}),
            "email_phu_huynh": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Nhập email phụ huynh"}),
        }


class ClassroomAssignForm(forms.Form):
    classroom = forms.ModelChoiceField(
        queryset=LopHoc.objects.all(),
        required=True,
        label="Chọn lớp",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, student, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        self.fields['classroom'].queryset = LopHoc.objects.all()


class HSProfileForm(forms.ModelForm):
    class Meta:
        model = HocSinh
        fields = ["ho_ten", "ngay_sinh", "gioi_tinh", "lop", "email_phu_huynh"]
        labels = {
            "ho_ten": "Họ tên",
            "gioi_tinh": "Giới tính",
            "ngay_sinh": "Ngày sinh",
            "lop": "Lớp",
            "email_phu_huynh": "Email phụ huynh",
        }
        widgets = {
            "ho_ten": forms.TextInput(attrs={"class": "form-control"}),
            "ngay_sinh": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "gioi_tinh": forms.Select(attrs={"class": "form-select"}),
            "lop": forms.Select(attrs={"class": "form-select"}),
            "email_phu_huynh": forms.EmailInput(attrs={"class": "form-control"}),
        }


class HSAvatarUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar"]
        widgets = {
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"})
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    # Giữ nguyên behavior của Django
    pass
