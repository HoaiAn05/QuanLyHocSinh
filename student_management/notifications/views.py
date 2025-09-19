from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import ThongBao
from students.models import HocSinh
from .forms import ThongBaoForm
from django.contrib.auth.decorators import login_required


# 2. Gửi thông báo chung cho tất cả phụ huynh
@login_required
def gui_thong_bao(request):
    if request.method == 'POST':
        form = ThongBaoForm(request.POST)
        if form.is_valid():
            tb = form.save()

            # Lấy tất cả email phụ huynh
            emails = list(HocSinh.objects.values_list('email_phu_huynh', flat=True))
            send_mail(tb.tieu_de, tb.noi_dung, settings.DEFAULT_FROM_EMAIL, emails)

            return redirect('danh_sach_thong_bao')
    else:
        form = ThongBaoForm()

    return render(request, 'notifications/gui_thong_bao.html', {'form': form})


@login_required
def danh_sach_thong_bao(request):
    ds = ThongBao.objects.all().order_by('-ngay_gui')
    return render(request, 'notifications/danh_sach_thong_bao.html', {'ds': ds})

@login_required
def chi_tiet_thong_bao(request, id):
    tb = get_object_or_404(ThongBao, id=id)
    return render(request, 'notifications/chi_tiet_thong_bao.html', {'tb': tb})


@login_required
def xoa_thong_bao(request, id):
    tb = get_object_or_404(ThongBao, id=id)
    if request.method == 'POST':
        tb.delete()
        return redirect('danh_sach_thong_bao')
    return render(request, 'notifications/xoa_thong_bao.html', {'tb': tb})