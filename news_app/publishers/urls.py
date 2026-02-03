from django.urls import path
from .views import (
    PublisherCreateView, PublisherListView,
    PublisherUpdateView
)

urlpatterns = [
    path(
        'publishers/', PublisherListView.as_view(),
        name='publisher-list',
        ),
    path(
        'publishers/create/', PublisherCreateView.as_view(),
        name='publisher-create',
        ),
    path(
        'publisher/<int:pk>/edit', PublisherUpdateView.as_view(),
        name='publisher-update',
        ),
]
