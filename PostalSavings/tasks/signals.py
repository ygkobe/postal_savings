from celery.signals import task_success, task_failure
from .models import Task


@task_success.connect
def task_success_handler(sender, result, **kwargs):
    """任务成功时更新 status 为 SUCCESS"""
    task_id = sender.request.id
    try:
        task = Task.objects.get(task_id=task_id)
        task.status = 'SUCCESS'
        task.save()
        print(f"Task {task_id} status updated to SUCCESS")
    except Task.DoesNotExist:
        print(f"Task with task_id {task_id} not found")


@task_failure.connect
def task_failure_handler(sender, exception, **kwargs):
    """任务失败时更新 status 为 FAILURE"""
    task_id = sender.request.id
    try:
        task = Task.objects.get(task_id=task_id)
        task.status = 'FAILURE'
        task.save()
        print(f"Task {task_id} status updated to FAILURE")
    except Task.DoesNotExist:
        print(f"Task with task_id {task_id} not found")