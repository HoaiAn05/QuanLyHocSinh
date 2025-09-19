from rest_framework import serializers
from .models import Diem

class DiemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diem
        fields = '__all__'
