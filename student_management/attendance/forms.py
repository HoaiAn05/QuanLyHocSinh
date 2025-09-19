from django import forms
from .models import DiemDanh
from students.models import HocSinh
from classes.models import LopHoc


class DiemDanhForm(forms.ModelForm):
    class Meta:
        model = DiemDanh
        fields = ["hoc_sinh", "ngay", "trang_thai"]

    def __init__(self, *args, **kwargs):
        giao_vien = kwargs.pop("giao_vien", None)  # truyền từ view
        super().__init__(*args, **kwargs)

        if giao_vien:
            # Lấy tất cả lớp mà giáo viên làm chủ nhiệm
            lop_ids = LopHoc.objects.filter(giao_vien_chu_nhiem=giao_vien).values_list("id", flat=True)
            self.fields["hoc_sinh"].queryset = HocSinh.objects.filter(lop_id__in=lop_ids)
        else:
            # Nếu không phải GV chủ nhiệm (admin chẳng hạn) thì cho xem tất cả
            self.fields["hoc_sinh"].queryset = HocSinh.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        hoc_sinh = cleaned_data.get("hoc_sinh")
        ngay = cleaned_data.get("ngay")

        if hoc_sinh and ngay:
            if DiemDanh.objects.filter(hoc_sinh=hoc_sinh, ngay=ngay).exists():
                raise forms.ValidationError("Học sinh này đã có điểm danh cho ngày đã chọn.")

        return cleaned_data
