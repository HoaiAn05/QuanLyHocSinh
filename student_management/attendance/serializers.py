from rest_framework import serializers
from .models import DiemDanh

class DiemDanhSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiemDanh
        fields = '__all__'
