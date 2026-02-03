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
    ''' View for journalists to create new articles.

        :model: Article
        :form_class: The form used to create an article.
        :template_name: The template for rendering the article creation form.
        :success_url: The URL to redirect to upon successful article creation.
        :form_valid: Sets the author and approval status before saving.
        :get_form_kwargs: Passes the current user to the form for any
            user-specific logic
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
    ''' View for listing all approved articles for the readers.

        :model: Article
        :template_name: The template for rendering the list of articles.
        :context_object_name: The context variable name for the list of
            articles.
        :get_queryset: Returns only approved articles.
    '''
    model = Article
    template_name = 'articles/reader_article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Return only articles that are approved
        return Article.objects.filter(approved=True)


class ReaderArticleDetailView(DetailView):
    '''View for displaying the details of a specific article to readers.

        :model: Article
        :template_name: The template for rendering the article details.
        :context_object_name: The context variable name for the article.
        :get_queryset: Returns only approved articles.
        :get_context_data: Adds subscription status to the context if the
            user is a reader.
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
    ''' A view that allows journalists the ability to view all
        articles.

        :model: Article
        :template_name: The template for rendering the list of articles.
        :context_object_name: The context variable name for the list of
            articles.
        :get_queryset: Returns articles authored by the logged-in journalist.
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
    '''A view that allows journalists to update their own articles

        :model: allows the Article model to be used.
        :form_class: The form used to update an article.
        :template_name: The template for rendering the article update form.
        :success_url: The URL to redirect to upon successful article update.
        :get_queryset: Returns articles authored by the logged-in journalist
            that are not yet approved.
        :get_form_kwargs: Passes the current user to the form for any
            user-specific logic.
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
    '''View for a journalist to delete their articles.

        :model: Article
        :template_name: The template for rendering the delete confirmation.
        :success_url: The URL to redirect to upon successful deletion.
        :get_queryset: Returns articles authored by the logged-in journalist
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
    '''A view to allow editors to view a list of articles.

        :model: Article
        :template_name: The template for rendering the list of articles.
        :context_object_name: The context variable name for the list of
            articles.
        :get_queryset: Returns articles that are either independent or
            belong to publishers the editor is associated with.
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
    '''A view to allow editors to delete articles.

        :model: Article
        :template_name: The template for rendering the delete confirmation.
        :success_url: The URL to redirect to upon successful deletion.
        :get_queryset: Returns articles that are either independent or
            belong to publishers the editor is associated with.
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
    '''A view that will allow editors to view and edit the articles posted for
        review and approve them at the same time.

        :model: Article
        :form_class: The form used to review and approve an article.
        :template_name: The template for rendering the article review form.
        :success_url: The URL to redirect to upon successful article review.
        :get_queryset: Returns articles that are either independent or
            belong to publishers the editor is associated with.
        :get_form_kwargs: Passes the current user to the form for any
            user-specific logic.
        :form_valid: Sets the article as approved if the 'approved' button
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
