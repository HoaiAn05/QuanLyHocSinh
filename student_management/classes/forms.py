from django import forms
from .models import LopHoc, PhanCongGiangDay
from scores.models import NamHoc
from teachers.models import GiaoVien

class LopHocForm(forms.ModelForm):
    class Meta:
        model = LopHoc
        fields = ["name", "giao_vien_chu_nhiem", "nam_hoc"]   #  thêm năm học
        labels = {
            "name": "Tên lớp",
            "giao_vien_chu_nhiem": "Giáo viên chủ nhiệm",
            "nam_hoc": "Năm học",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lấy danh sách giáo viên
        self.fields["giao_vien_chu_nhiem"].queryset = GiaoVien.objects.all()


class PhanCongForm(forms.ModelForm):
    nam_hoc = forms.ModelChoiceField(
        queryset=NamHoc.objects.all(),
        required=True,
        label="Năm học"
    )

    class Meta:
        model = PhanCongGiangDay
        fields = ['nam_hoc', 'lop', 'mon_hoc', 'giao_vien']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ban đầu: nếu chưa chọn năm học thì lớp để trống
        self.fields['lop'].queryset = LopHoc.objects.none()

        # Nếu có dữ liệu POST (người dùng chọn năm học)
        if 'nam_hoc' in self.data:
            try:
                nam_hoc_id = int(self.data.get('nam_hoc'))
                self.fields['lop'].queryset = LopHoc.objects.filter(nam_hoc_id=nam_hoc_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:  # khi edit phân công đã có sẵn
            self.fields['lop'].queryset = LopHoc.objects.filter(nam_hoc=self.instance.nam_hoc)


from django import forms
from .models import TietHoc
from teachers.models import GiaoVien
from .models import LopHoc
from subjects.models import MonHoc
from .models import PhanCongGiangDay


class TietHocForm(forms.ModelForm):
    thu = forms.ChoiceField(
        choices=[(2, "Thứ 2"), (3, "Thứ 3"), (4, "Thứ 4"),
                 (5, "Thứ 5"), (6, "Thứ 6"), (7, "Thứ 7")],
        label="Thứ"
    )
    tiet = forms.ChoiceField(
        choices=[(1, "Tiết 1"), (2, "Tiết 2"), (3, "Tiết 3"),
                 (4, "Tiết 4"), (5, "Tiết 5"), (6, "Tiết 6"),
                 (7, "Tiết 7"), (8, "Tiết 8")],
        label="Tiết học"
    )

    class Meta:
        model = TietHoc
        fields = ["thu", "tiet", "phan_cong"]
        labels = {
            "phan_cong": "Phân công",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phan_cong"].queryset = PhanCongGiangDay.objects.select_related(
            "lop", "mon_hoc", "giao_vien"
        )
        self.fields["phan_cong"].label_from_instance = (
            lambda obj: f"{obj.lop.name} - {obj.mon_hoc.ten_mon} ({obj.giao_vien.ho_ten})"
        )

    def clean(self):
        cleaned_data = super().clean()
        thu = cleaned_data.get("thu")
        tiet = cleaned_data.get("tiet")
        phan_cong = cleaned_data.get("phan_cong")

        if thu and tiet and phan_cong:
            lop = phan_cong.lop
            exists = TietHoc.objects.filter(
                thu=thu, tiet=tiet, phan_cong__lop=lop
            ).exclude(pk=self.instance.pk).exists()

            if exists:
                raise forms.ValidationError(
                    f"Lớp {lop.name} đã có môn khác ở Thứ {thu}, Tiết {tiet}!"
                )

        return cleaned_data