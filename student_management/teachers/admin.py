from django.contrib import admin
from .models import GiaoVien

@admin.register(GiaoVien)
class GiaoVienAdmin(admin.ModelAdmin):
    list_display = ( 'ho_ten', 'email', 'mon_day')
    search_fields = ( 'ho_ten',)
