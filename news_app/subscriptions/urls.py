from django.urls import path
from .views import (
    ReaderSubscriptionsView,
    SubscribedJournalistArticleListView,
    SubscribedNewsletterArticleListView,
    SubscribeJournalistView,
    SubscribeNewsletterView,
)

urlpatterns = [
    # reader dashboard
    path(
        'reader/subscriptions/',
        ReaderSubscriptionsView.as_view(),
        name='reader-subscriptions'
        ),
    # Article and Newsletter lists (GET)
    path(
        'reader/subscriptions/journalist/<int:journalist_id>/',
        SubscribedJournalistArticleListView.as_view(),
        name='subscribed-journalist-articles'
        ),
    path(
        'reader/subscriptions/newsletter/<int:newsletter_id>/',
        SubscribedNewsletterArticleListView.as_view(),
        name='subscribed-newsletter-articles'
        ),
    # Article and Newsletter subscriptions (POST)
    path(
        'subscribe/journalist/<int:journalist_id>/',
        SubscribeJournalistView.as_view(),
        name='subscribe-journalist'
        ),
    path(
        'subscribe/newsletter/<int:newsletter_id>/',
        SubscribeNewsletterView.as_view(),
        name='subscribe-newsletter'
        ),
]
