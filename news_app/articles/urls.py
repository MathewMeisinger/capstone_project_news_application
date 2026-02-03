from django.urls import path
from .views import (
    ArticleCreateView,
    ApprovedArticleListView,
    JournalistArticleUpdateView, JournalistArticleListView,
    JournalistDeleteView, EditorArticleDeleteView,
    EditorArticleListView,
    EditorArticleReviewView,
    ReaderArticleDetailView,
)

urlpatterns = [
    path('articles/create/',
         ArticleCreateView.as_view(),
         name='article-create'
         ),
    path('articles/',
         ApprovedArticleListView.as_view(),
         name='approved-articles'
         ),
    path(
         'articles/<int:pk>/',
         ReaderArticleDetailView.as_view(),
         name='reader-article-detail'
         ),
    path('journalist/articles/',
         JournalistArticleListView.as_view(),
         name='journalist-articles'
         ),
    path(
         'journalist/articles/<int:pk>/edit/',
         JournalistArticleUpdateView.as_view(),
         name='article-update'
         ),
    path(
         'journalist/articles/<int:pk>/delete/',
         JournalistDeleteView.as_view(),
         name='article-delete'
    ),
    path(
         'editor/articles/',
         EditorArticleListView.as_view(),
         name='editor-articles',
         ),
    path(
         'editor/articles/<int:pk>/delete/',
         EditorArticleDeleteView.as_view(),
         name='editor-article-delete',
         ),
    path(
         'editor/articles/<int:pk>/review/',
         EditorArticleReviewView.as_view(),
         name='editor-article-review',
         ),
]
