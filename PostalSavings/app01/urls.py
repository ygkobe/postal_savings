from django.urls import path
from .views import BookListView, AllBookListView
from .views import trigger_tasks

urlpatterns = [
    path('page/', BookListView.as_view(), name='page-book-list'),
    path('all/', AllBookListView.as_view(), name='all-book-list'),
    path('trigger/', trigger_tasks, name='trigger_tasks'),
]