from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import BookSerializer


class BookListView(APIView):
    def get(self, request):
        # 获取所有书籍
        queryset = Book.objects.all()
        # 创建分页器实例
        paginator = PageNumberPagination()
        # 对查询集进行分页
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            # 如果有分页数据，序列化分页后的数据
            serializer = BookSerializer(instance=page, many=True)
            return paginator.get_paginated_response(serializer.data)
        # 如果没有分页数据，序列化原始查询集
        serializer = BookSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class AllBookListView(APIView):
    def get(self, request):
        # 获取所有书籍，不进行分页
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)


# views.py
from django.http import JsonResponse
from .tasks import send_email_task, process_data_task


def trigger_tasks(request):
    # 触发邮件任务
    email_result = send_email_task.delay('user@example.com')
    # 触发数据处理任务
    data_result = process_data_task.delay('some_data')

    return JsonResponse({
        'email_task_id': email_result.id,
        'data_task_id': data_result.id,
        'message': 'Tasks have been triggered!'
    })