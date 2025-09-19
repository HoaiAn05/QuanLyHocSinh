from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import DiemDanh

@receiver(post_save, sender=DiemDanh)
def thong_bao_vang_hoc(sender, instance, created, **kwargs):
    """
    Khi lưu điểm danh, nếu trạng thái là 'vang' thì gửi email cho phụ huynh
    """
    if instance.trang_thai == "vang" and instance.hoc_sinh.email_phu_huynh:
        hoc_sinh = instance.hoc_sinh
        subject = f"Thông báo vắng học - {hoc_sinh.ho_ten}"
        message = (
            f"Kính gửi phụ huynh,\n\n"
            f"Học sinh {hoc_sinh.ho_ten} (lớp {hoc_sinh.lop}) đã vắng học vào ngày {instance.ngay}.\n"
            f"Xin quý phụ huynh lưu ý.\n\n"
            f"Trân trọng."
        )
        send_mail(
            subject,
            message,
            None,  # lấy từ DEFAULT_FROM_EMAIL
            [hoc_sinh.email_phu_huynh],
            fail_silently=False,
        )
