from django.shortcuts import render
from django.views.generic import (
    CreateView, ListView, UpdateView,
    DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from users.mixins import JournalistRequiredMixin, EditorRequiredMixin
from .models import Newsletter
from .forms import NewsletterForm
from subscriptions.models import NewsletterSubscription


class JournalistNewsletterListView(
    LoginRequiredMixin,
    JournalistRequiredMixin,
    ListView
):
    ''' A view to allow Journalists to view newsletters
        they have created.

        :model: Newsletter
        :template_name: The template to render the list of newsletters.
        :context_object_name: The context variable name for the list of
            newsletters.
        :get_queryset: Method to filter newsletters by the current user.
    '''
    model = Newsletter
    template_name = 'newsletters/journalist_newsletter_list.html'
    context_object_name = 'newsletters'

    def get_queryset(self):
        return Newsletter.objects.filter(author=self.request.user)


class JournalistNewsletterCreateView(
    LoginRequiredMixin,
    CreateView,
    JournalistRequiredMixin,
):
    ''' A view to allow Journalists to create newsletters.

        :model: Newsletter
        :form_class: The form class to use for creating newsletters.
        :template_name: The template to render the newsletter creation form.
        :success_url: The URL to redirect to upon successful creation.
        :get_form_kwargs: Method to pass the current user to the form.
        :form_valid: Method to set the author of the newsletter before saving.
    '''
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletters/newsletter_form.html'
    success_url = reverse_lazy('journalist-newsletters')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


class JournalistNewsletterUpdateView(
    LoginRequiredMixin,
    UpdateView,
    JournalistRequiredMixin
):
    ''' A view to allow Journalists to update newsletters they created.

        :model: Newsletter
        :form_class: The form class to use for updating newsletters.
        :template_name: The template to render the newsletter update form.
        :success_url: The URL to redirect to upon successful update.
        :get_queryset: Method to filter newsletters by the current user.
        :get_form_kwargs: Method to pass the current user to the form.
    '''
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletters/newsletter_form.html'
    success_url = reverse_lazy('journalist-newsletters')

    def get_queryset(self):
        return Newsletter.objects.filter(author=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class JournalistNewsletterDeleteView(
    JournalistRequiredMixin,
    LoginRequiredMixin,
    DeleteView
):
    ''' View to allow journalists to delete their own newsletters.

        :model: Newsletter
        :template_name: The template to render the newsletter deletion
            confirmation.
        :success_url: The URL to redirect to upon successful deletion.
        :get_queryset: Method to filter newsletters by the current user.
    '''
    model = Newsletter
    template_name = 'newsletters/newsletter_confirm_delete.html'
    success_url = reverse_lazy('journalist-newsletters')

    def get_queryset(self):
        return Newsletter.objects.filter(author=self.request.user)


class EditorNewsletterListView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    ListView
):
    ''' A view to allow editors to view Newsletters.

        :model: Newsletter
        :template_name: The template to render the list of newsletters.
        :context_object_name: The context variable name for the list of
            newsletters.
    '''
    model = Newsletter
    template_name = 'newsletters/editor_newsletter_list.html'
    context_object_name = 'newsletters'


class EditorNewsletterCreateView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    CreateView
):
    ''' A view to allow editors to create newsletters

        :model: Newsletter
        :form_class: The form class to use for creating newsletters.
        :template_name: The template to render the newsletter creation form.
        :success_url: The URL to redirect to upon successful creation.
        :get_form_kwargs: Method to pass the current user to the form.
        :form_valid: Method to set the author of the newsletter before saving.
    '''
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletters/newsletter_form.html'
    success_url = reverse_lazy('editor-newsletters')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


class EditorNewsletterUpdateView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    UpdateView
):
    ''' A view to allow editors to edit the newsletters

        :model: Newsletter
        :form_class: The form class to use for updating newsletters.
        :template_name: The template to render the newsletter update form.
        :success_url: The URL to redirect to upon successful update.
        :get_form_kwargs: Method to pass the current user to the form.
    '''
    model = Newsletter
    form_class = NewsletterForm
    template_name = 'newsletters/newsletter_form.html'
    success_url = reverse_lazy('editor-newsletters')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditorNewsletterDeleteView(
  LoginRequiredMixin,
  EditorRequiredMixin,
  DeleteView
):
    ''' A view that will allow editors to delete Newsletters.

        :model: Newsletter
        :template_name: The template to render the newsletter deletion
            confirmation.
        :success_url: The URL to redirect to upon successful deletion.
        :get_queryset: Method to filter newsletters by the current user.
    '''
    model = Newsletter
    template_name = 'newsletters/newsletter_confirm_delete.html'
    success_url = reverse_lazy('editor-newsletters')

    def get_queryset(self):
        return Newsletter.objects.all()


class ReaderNewsletterListView(
    LoginRequiredMixin,
    ListView
):
    ''' A view to allow readers to view newsletters they are subscribed to.

        :model: Newsletter
        :template_name: The template to render the list of newsletters.
        :context_object_name: The context variable name for the list of
            newsletters.
    '''
    model = Newsletter
    template_name = 'newsletters/reader_newsletter_list.html'
    context_object_name = 'newsletters'


class ReaderNewsletterDetailView(
    LoginRequiredMixin,
    DetailView
):
    ''' A view to allow readers to view a specific newsletter they are
        subscribed to.

        :model: Newsletter
        :template_name: The template to render the newsletter detail view.
        :def get_context_data: Method to add additional context data,
            including articles and subscription status.
    '''
    model = Newsletter
    template_name = 'newsletters/reader_newsletter_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = self.object.articles.filter(approved=True)

        if self.request.user.is_authenticated and self.request.user.role == 'reader':
            context['is_subscribed'] = NewsletterSubscription.objects.filter(
                reader=self.request.user,
                newsletter=self.object
            ).exists()

        return context
