from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from users.mixins import EditorRequiredMixin
from .models import Publisher
from .forms import PublisherForm


class PublisherCreateView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    CreateView
):
    '''
    A view that will allow editors to create a publisher and add
    editors and journalists to that publisher at time of creation.
    '''
    model = Publisher
    form_class = PublisherForm
    template_name = 'publishers/publisher_form.html'
    success_url = reverse_lazy('publisher-list')


class PublisherUpdateView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    UpdateView
):
    '''
    A view to allow editors to add journalists or editors to the publisher
    after creation.
    '''
    model = Publisher
    form_class = PublisherForm
    template_name = 'publishers/publisher_form.html'
    success_url = reverse_lazy('publisher-list')


class PublisherListView(
    LoginRequiredMixin,
    EditorRequiredMixin,
    ListView
):
    '''
    A view for editors to see a list of the publishers.
    '''
    model = Publisher
    template_name = 'publishers/publisher_list.html'
    context_object_name = 'publishers'
