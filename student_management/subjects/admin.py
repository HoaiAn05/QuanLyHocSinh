from django.contrib import admin
from .models import MonHoc

@admin.register(MonHoc)
class MonHocAdmin(admin.ModelAdmin):
    list_display = ('ma_mon', 'ten_mon')
    search_fields = ('ma_mon', 'ten_mon')
