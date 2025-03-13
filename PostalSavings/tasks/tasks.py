from celery import shared_task
import time
from .models import Task


@shared_task(bind=True)
def create_task(self, instance_id):
    """异步处理任务，不创建实例"""
    print("异步创建 Task 实例")
    time.sleep(5)
    print("创建成功")
    return instance_id


@shared_task(bind=True)
def update_task(self, task_id, validated_data):
    """异步更新 Task 实例"""
    print("异步更新 Task 实例")
    time.sleep(5)
    try:
        task = Task.objects.get(id=task_id)
        task.title = validated_data.get('title', task.title)
        task.description = validated_data.get('description', task.description)
        task.completed = validated_data.get('completed', task.completed)
        task.save()
        print("更新成功")
        return task.id
    except Task.DoesNotExist:
        return None
