from rest_framework import serializers
from .models import GiaoVien

class GiaoVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiaoVien
        fields = '__all__'
