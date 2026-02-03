from django.urls import path
from .views import (
    ArticleListCreateAPIView,
    ArticleDetailAPIView,
    SubscribedArticleListAPIView
)

urlpatterns = [
    path('articles/', ArticleListCreateAPIView.as_view()),
    path('articles/<int:pk>/', ArticleDetailAPIView.as_view()),
    path('articles/subscribed/', SubscribedArticleListAPIView.as_view()),
]
