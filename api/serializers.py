from rest_framework import serializers
from .models import Notice,Attendance
import pandas as pd
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

    def validate_visible(self, value):
        if value and Notice.objects.filter(visible=True).count() >= 4:
            raise serializers.ValidationError("Only 4 notices can be visible at a time.")
        return value

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def process_excel(self, file):
        df = pd.read_excel(file)
        return df.to_dict(orient='records')