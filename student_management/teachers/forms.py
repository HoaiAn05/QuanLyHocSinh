# teachers/forms.py
from django import forms
from accounts.models import User
from .models import GiaoVien
from django.contrib.auth.forms import PasswordChangeForm

class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.role = "teacher"
        teacher.set_password(self.cleaned_data["password"])
        if commit:
            teacher.save()
        return teacher

class GiaoVienProfileForm(forms.ModelForm):
    class Meta:
        model = GiaoVien
        fields = ["ho_ten", "email", "so_dien_thoai", "mon_day"]
        labels = {
            "ho_ten": "Họ tên",
            "email": "Email",
            "so_dien_thoai": "Số điện thoại",
            "mon_day": "Môn dạy",
        }

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar"]

class CustomPasswordChangeForm(PasswordChangeForm):
    # Giữ nguyên behavior của Django
    pass