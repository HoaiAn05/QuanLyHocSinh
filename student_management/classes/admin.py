from django.contrib import admin
from .models import LopHoc

@admin.register(LopHoc)
class LopHocAdmin(admin.ModelAdmin):
    list_display = ('name', 'giao_vien_chu_nhiem')
    search_fields = ('name',)
    list_filter = ('name',)
