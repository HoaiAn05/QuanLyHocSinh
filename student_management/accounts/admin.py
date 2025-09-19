from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import User


@admin.register(User)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_active')

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.password = make_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
