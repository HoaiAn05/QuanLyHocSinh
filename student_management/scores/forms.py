from django import forms
from classes.models import LopHoc
from .models import NamHoc, HocKy
from classes.models import PhanCongGiangDay  # model phân công giảng dạy

class LopNamHocForm(forms.Form):
    lop = forms.ModelChoiceField(queryset=LopHoc.objects.none(), label="Lớp")
    nam_hoc = forms.ModelChoiceField(queryset=NamHoc.objects.none(), label="Năm học")
    hoc_ky = forms.ModelChoiceField(queryset=HocKy.objects.all(), label="Học kỳ")

    def __init__(self, *args, **kwargs):
        giao_vien = kwargs.pop('giao_vien', None)  # truyền từ view
        super().__init__(*args, **kwargs)

        if giao_vien:
            # Lọc lớp và năm học theo giáo viên được phân công
            phan_cong = PhanCongGiangDay.objects.filter(giao_vien=giao_vien)
            self.fields['lop'].queryset = LopHoc.objects.filter(
                id__in=phan_cong.values_list('lop_id', flat=True)
            ).distinct()
            self.fields['nam_hoc'].queryset = NamHoc.objects.filter(
                id__in=phan_cong.values_list('nam_hoc_id', flat=True)
            ).distinct()
