import datetime
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']  # task_id 和 status 可写

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.task_id = validated_data.get('task_id', instance.task_id)  # 更新 task_id
        instance.status = validated_data.get('status', instance.status)    # 更新 status
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['current_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return representation