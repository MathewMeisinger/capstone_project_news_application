from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from users.mixins import ReaderRequiredMixin
from .models import JournalistSubscription, NewsletterSubscription
from articles.models import Article
from newsletters.models import Newsletter

User = get_user_model()


class ReaderSubscriptionsView(
    LoginRequiredMixin,
    ReaderRequiredMixin,
    TemplateView
):
    '''
    View to display the subscriptions of a reader.
    Shows both journalist and newsletter subscriptions.
    '''
    template_name = 'subscriptions/reader_subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reader = self.request.user

        context['journalist_subscriptions'] = JournalistSubscription.objects.filter(
            reader=reader
        )

        context['newsletter_subscriptions'] = NewsletterSubscription.objects.filter(
            reader=reader
        )

        return context


class SubscribedJournalistArticleListView(
    LoginRequiredMixin,
    ReaderRequiredMixin,
    ListView
):
    '''
    View to display articles from journalists the reader is subscribed to.
    '''
    model = Article
    template_name = 'subscriptions/journalist_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        journalist = get_object_or_404(
            User,
            id=self.kwargs['journalist_id'],
            role='journalist'
        )
        return Article.objects.filter(
            author=journalist,
            approved=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journalist'] = User.objects.get(
            id=self.kwargs['journalist_id']
        )
        return context


class SubscribedNewsletterArticleListView(
    LoginRequiredMixin,
    ReaderRequiredMixin,
    ListView
):
    '''
    View to display articles from newsletters the reader is subscribed to.
    '''
    model = Article
    template_name = 'subscriptions/newsletter_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        newsletter = get_object_or_404(
            Newsletter,
            id=self.kwargs['newsletter_id']
        )
        return newsletter.articles.filter(
            approved=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter'] = Newsletter.objects.get(
            id=self.kwargs['newsletter_id']
        )
        return context


class SubscribeJournalistView(
    LoginRequiredMixin,
    ReaderRequiredMixin,
    View
):
    '''
    View to handle subscribing a reader to a journalist.
    '''
    def post(self, request, journalist_id):
        JournalistSubscription.objects.get_or_create(
            reader=request.user,
            journalist_id=journalist_id
        )
        return redirect('reader-subscriptions')


class SubscribeNewsletterView(
    LoginRequiredMixin,
    ReaderRequiredMixin,
    View
):
    '''
    View to handle subscribing a reader to a newsletter.
    '''
    def post(self, request, newsletter_id):
        NewsletterSubscription.objects.get_or_create(
            reader=request.user,
            newsletter_id=newsletter_id
        )
        return redirect('reader-subscriptions')
