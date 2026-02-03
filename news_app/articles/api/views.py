from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from articles.models import Article
from .serializers import ArticleSerializer, ArticleWriteSerializer
from .permissions import IsAuthorOrEditor, IsJournalist
from subscriptions.models import JournalistSubscription, NewsletterSubscription
from django.db.models import Q


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    '''
    API view to list all articles and allow journalists to create new articles.
    '''
    queryset = Article.objects.filter(approved=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleWriteSerializer
        return ArticleSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsJournalist()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            approved=False
            )


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    API view to retrieve a specific article by its ID.
    '''
    queryset = Article.objects.filter(approved=True)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ArticleWriteSerializer
        return ArticleSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAuthorOrEditor()]

    def get_queryset(self):
        if self.request.method in SAFE_METHODS:
            return Article.objects.filter(approved=True)
        return Article.objects.all()


class SubscribedArticleListAPIView(generics.ListAPIView):
    '''
    API view to list articles from journalists and newsletters the user is
    subscribed to.
    '''
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        journalist_ids = JournalistSubscription.objects.filter(
            reader=user
        ).values_list('journalist_id', flat=True)

        newsletter_articles = NewsletterSubscription.objects.filter(
            reader=user
        ).values_list('newsletter__articles__id', flat=True)

        return Article.objects.filter(
            Q(author_id__in=journalist_ids) |
            Q(id__in=newsletter_articles),
            approved=True
        ).distinct()
