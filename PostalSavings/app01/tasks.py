# myapp/tasks.py
from celery import shared_task
from time import sleep


@shared_task(name='app01.tasks.send_email_task')
def send_email_task(recipient):
    print(f"发送邮件给 {recipient}...")
    sleep(2)  # 模拟耗时操作
    return f"邮件已发送给 {recipient}"


@shared_task(name='app01.tasks.process_data_task')
def process_data_task(data):
    print(f"处理数据: {data}...")
    sleep(3)  # 模拟耗时操作
    return f"数据 {data} 已处理"
