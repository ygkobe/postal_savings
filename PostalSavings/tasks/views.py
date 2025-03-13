from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from .models import Task
from .serializers import TaskSerializer
from .tasks import create_task, update_task
from common.logs import logger


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        logger.info("Fetching all tasks")
        try:
            response = super().get(request, *args, **kwargs)
            logger.info(f"Successfully retrieved {self.queryset.count()} tasks")
            return response
        except Exception as e:
            logger.error(f"Failed to fetch tasks: {str(e)}")
            return Response(
                {"message": f"Error retrieving tasks: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.info(f"Creating task with data: {serializer.validated_data}")
            # 先创建实例并保存 task_id 和 status
            instance = Task.objects.create(
                title=serializer.validated_data.get('title', ''),
                description=serializer.validated_data.get('description', ''),
                completed=serializer.validated_data.get('completed', False),
                task_id='',  # 先留空，待 Celery 任务分配
                status='PENDING'
            )
            task = create_task.delay(instance.id)  # 传递 instance.id 而不是 validated_data
            instance.task_id = task.id  # 更新 task_id
            instance.save()
            return Response(
                {
                    'message': 'Task creation queued',
                    'task_id': task.id,
                    'instance_id': instance.id
                },
                status=status.HTTP_202_ACCEPTED
            )
        logger.warning(f"Invalid data received: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            logger.info(f"Updating task {instance.id} with data: {serializer.validated_data}")
            task = update_task.delay(instance.id, serializer.validated_data)
            instance.task_id = task.id
            instance.status = 'PENDING'
            instance.save()
            return Response(
                {
                    'message': 'Task update queued',
                    'task_id': task.id
                },
                status=status.HTTP_202_ACCEPTED
            )
        logger.warning(f"Update failed for task {instance.id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskStatusView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        try:
            result = AsyncResult(task_id)
            logger.info(f"Checking status for task_id: {task_id}")
            response_data = {
                'task_id': task_id,
                'status': result.status,
            }

            if result.ready():
                if result.successful():
                    task_result = result.result
                    try:
                        task_instance = Task.objects.get(id=task_result)
                        serializer = TaskSerializer(task_instance)
                        response_data.update({
                            'status': task_instance.status,
                            'result': serializer.data,
                            'message': 'Task completed successfully'
                        })
                        logger.info(f"Task {task_id} completed successfully")
                    except Task.DoesNotExist:
                        response_data.update({
                            'status': 'SUCCESS',
                            'result': {'task_instance_id': task_result},
                            'message': 'Task completed but instance not found'
                        })
                        logger.warning(f"Task {task_id} completed but Task instance not found")
                else:
                    response_data.update({
                        'status': 'FAILURE',
                        'error': str(result.result),
                        'message': 'Task failed'
                    })
                    logger.error(f"Task {task_id} failed: {str(result.result)}")
            else:
                response_data.update({
                    'message': 'Task is still processing',
                    'progress': result.info if hasattr(result, 'info') else None
                })
                logger.info(f"Task {task_id} is still processing")

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving task status {task_id}: {str(e)}")
            return Response(
                {
                    'task_id': task_id,
                    'status': 'UNKNOWN',
                    'message': f'Error retrieving task status: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
