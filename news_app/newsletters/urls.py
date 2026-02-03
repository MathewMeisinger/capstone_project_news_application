from django.urls import path
from .views import (
    JournalistNewsletterCreateView,
    JournalistNewsletterDeleteView,
    JournalistNewsletterListView,
    JournalistNewsletterUpdateView,
    EditorNewsletterDeleteView,
    EditorNewsletterUpdateView,
    EditorNewsletterListView,
    EditorNewsletterCreateView,
    ReaderNewsletterDetailView,
    ReaderNewsletterListView,
)

urlpatterns = [
    # Reader URLS
    path(
        'newsletters/',
        ReaderNewsletterListView.as_view(),
        name='reader-newsletters'
        ),
    path(
        'newsletters/<int:pk>/',
        ReaderNewsletterDetailView.as_view(),
        name='reader-newsletter-detail'
        ),
    # Journalist URLS
    path(
        'journalist/newsletters',
        JournalistNewsletterListView.as_view(),
        name='journalist-newsletters'
        ),
    path('newsletters/create/',
         JournalistNewsletterCreateView.as_view(),
         name='journalist-newsletter-create'
         ),
    path(
        'journalist/newsletters/<int:pk>/edit/',
        JournalistNewsletterUpdateView.as_view(),
        name='journalist-newsletter-update',
        ),
    path(
        'journalist/newsletters/<int:pk>/delete/',
        JournalistNewsletterDeleteView.as_view(),
        name='journalist-newsletter-delete',
        ),
    # Editor URLS
    path(
         'editor/newsletters/',
         EditorNewsletterListView.as_view(),
         name='editor-newsletters',
         ),
    path(
        'editor/newsletters/create/',
        EditorNewsletterCreateView.as_view(),
        name='editor-newsletter-create',
        ),
    path(
         'editor/newsletters/<int:pk>/edit/',
         EditorNewsletterUpdateView.as_view(),
         name='editor-newsletter-update',
         ),
    path(
         'editor/newsletters/<int:pk>/delete/',
         EditorNewsletterDeleteView.as_view(),
         name='editor-newsletter-delete',
         ),
]
