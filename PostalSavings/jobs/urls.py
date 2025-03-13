from django.urls import path
from .views import JobListCreateAPIView, JobRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('list/', JobListCreateAPIView.as_view(), name='job-list-create'),
    path('list/<int:pk>/', JobRetrieveUpdateDestroyAPIView.as_view(), name='job-retrieve-update-destroy'),
]