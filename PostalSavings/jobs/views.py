from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializers import JobSerializer
from common.logs import logger
import os


class JobListCreateAPIView(APIView):
    def get(self, request):
        # 获取当前文件名

        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        job = JobSerializer(data=request.data)
        current_function = self.get.__name__
        print(current_function)
        if job.is_valid():
            job.save()
            return Response(job.data, status=status.HTTP_201_CREATED)
        return Response(job.errors, status=status.HTTP_400_BAD_REQUEST)


class JobRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return None

    def get(self, request, pk):
        job = self.get_object(pk)
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = self.get_object(pk)
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = self.get_object(pk)
        if job is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)