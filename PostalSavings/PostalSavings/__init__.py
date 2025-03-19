# 假设你的项目名为 myproject，路径为 myproject/__init__.py
import pymysql

pymysql.install_as_MySQLdb()

from .celery import app as celery_app

__all__ = ('celery_app',)