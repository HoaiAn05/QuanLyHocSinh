from rest_framework import serializers
from .models import ThongBao

class ThongBaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThongBao
        fields = '__all__'
