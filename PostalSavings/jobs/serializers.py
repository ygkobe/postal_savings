import time
from rest_framework import serializers
from .models import Job
from django.utils import timezone


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        # fields = ['id', 'title', 'description', 'created_at']
        fields = "__all__"

    def to_internal_value(self, data):
        # 对输入数据进行预处理
        if 'created_at' in data:
            try:
                # 假设输入的日期时间格式为 'YYYY-MM-DD HH:MM:SS'
                data['created_at'] = timezone.datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise serializers.ValidationError({'created_at': '日期时间格式应为 YYYY-MM-DD HH:MM:SS'})
        return super().to_internal_value(data)

    def to_representation(self, instance):
        # 对输出数据进行格式化
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        representation['get_time'] = time.time()
        # 将 created_at 字段的值赋给新的字段名 creation_time
        representation['creation_time'] = representation.pop('created_at')
        return representation