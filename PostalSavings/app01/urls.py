from django.urls import path
from .views import BookListView, AllBookListView

urlpatterns = [
    path('page/', BookListView.as_view(), name='page-book-list'),
    path('all/', AllBookListView.as_view(), name='all-book-list'),
]