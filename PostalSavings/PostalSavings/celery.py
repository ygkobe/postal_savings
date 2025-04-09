import os
from celery import Celery

# 设置 Django 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PostalSavings.settings')

app = Celery('PostalSavings')

# 使用 Django 的配置文件来配置 Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()


# 配置任务路由
app.conf.task_routes = {
    'app01.tasks.send_email_task': {'queue': 'email_queue'},  # 邮件任务路由到 email_queue
    'app01.tasks.process_data_task': {'queue': 'data_queue'},  # 数据处理任务路由到 data_queue
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
