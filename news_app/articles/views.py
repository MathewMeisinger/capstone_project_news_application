from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, ListView, UpdateView,
    DeleteView, DetailView
)
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ArticleCreationForm
from users.mixins import (
    JournalistRequiredMixin,
    EditorRequiredMixin
)
from django.db.models import Q
from publishers.models import Publisher
from subscriptions.models import JournalistSubscription


class ArticleCreateView(
    LoginRequiredMixin,
    JournalistRequiredMixin,
    CreateView
):
    '''
    View for creating a new Article.
    Only accessible to logged-in users with journalist role.
    Uses ArticleCreationForm for input.
    On successful creation, redirects to the article detail page.
    '''
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('journalist-dashboard')

    def form_valid(self, form):
        # Set the author of the article to the current logged-in user
        form.instance.author = self.request.user
        # New articles are unapproved by default
        form.instance.approved = False
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ApprovedArticleListView(ListView):
    '''
    View for listing all approved articles for the readers.
    Accessible to all readers.
    Displays articles that are approved and can be read by readers.
    '''
    model = Article
    template_name = 'articles/reader_article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Return only articles that are approved
        return Article.objects.filter(approved=True)


class ReaderArticleDetailView(DetailView):
    '''
    View for displaying the details of a specific article to readers.
    Accessible to all readers.
    '''
    model = Article
    template_name = 'articles/reader_article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        # Return only approved articles
        return Article.objects.filter(approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (self.request.user.is_authenticated and
           self.request.user.role == 'reader'):
            context['is_subscribed'] = JournalistSubscription.objects.filter(
                reader=self.request.user,
                journalist=self.object.author
            ).exists()

        return context


class JournalistArticleListView(
    LoginRequiredMixin,
    JournalistRequiredMixin,
    ListView
):
    '''
    A view that allows journalists the ability to view all
    articles.
    '''
    model = Article
    template_name = 'articles/journalist_article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class JournalistArticleUpdateView(
    LoginRequiredMixin,
    JournalistRequiredMixin,
    UpdateView
):
    '''
    A view that allows journalists to update their own articles
    Articles that have not yet been approved can be edited.
    '''
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('journalist-articles')

    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user,
            approved=False
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class JournalistDeleteView(
    LoginRequiredMixin,
    JournalistRequiredMixin,
    DeleteView
):
    '''
    View for a journalist to delete their articles.
    Only articles that have not been approved by
    an editor can be deleted.
    '''
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('journalist-articles')

    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user,
            approved=False
        )


class EditorArticleListView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    ListView
):
    '''
    A view to allow editors to view a list of articles.
    Will include options specific to editors
    Will able to edit and approve articles from this view.
    '''
    model = Article
    template_name = 'articles/editor_article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        publishers = Publisher.objects.filter(editors=self.request.user)
        return Article.objects.filter(
            Q(publisher__in=publishers) |
            Q(publisher__isnull=True)
        )


class EditorArticleDeleteView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    DeleteView
):
    '''
    A view to allow editors to delete articles.
    Can delete all independent articles or articles that
    are within their publishers.
    '''
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('editor-articles')

    def get_queryset(self):
        publishers = Publisher.objects.filter(editors=self.request.user)
        return Article.objects.filter(
            Q(publisher__in=publishers) |
            Q(publisher__isnull=True)
        )


class EditorArticleReviewView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    UpdateView
):
    '''
    A view that will allow editors to view and edit the articles posted for
    review and approve them at the same time.
    '''
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articles/editor_article_review.html'
    success_url = reverse_lazy('editor-articles')

    def get_queryset(self):
        publishers = Publisher.objects.filter(editors=self.request.user)
        return Article.objects.filter(
            Q(publisher__in=publishers) |
            Q(publisher__isnull=True)
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if 'approved' in self.request.POST:
            self.object.approved = True

        self.object.save()
        form.save_m2m()

        return redirect(self.success_url)
