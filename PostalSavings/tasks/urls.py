from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskStatusView

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
]