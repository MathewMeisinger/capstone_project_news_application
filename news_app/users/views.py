from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from .models import User
from django.contrib.auth.models import Group
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from articles.models import Article


class RegisterView(CreateView):
    '''
    View to handle user registration.
    Utilizes the UserRegistrationForm to create a new user.
    On successful registration, redirects to the login page.
    '''
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        '''
        If the form is valid, save the new user and redirect to success URL.
        '''
        response = super().form_valid(form)
        role = form.cleaned_data.get('role')

        group = Group.objects.get(name=role.capitalize())
        self.object.groups.add(group)

        return response


class RoleRedirectView(View):
    '''
    Class to redirect the user to the appropriate dashboard.
    If a users role is reader, journalist or editor they will get
    different dahsboards.
    if no role then return login screen.
    '''

    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        if user.role == 'reader':
            return redirect('reader-dashboard')
        elif user.role == 'journalist':
            return redirect('journalist-dashboard')
        elif user.role == 'editor':
            return redirect('editor-dashboard')
        return redirect('login')


class ReaderDashboardView(LoginRequiredMixin, TemplateView):
    '''
    Dashboard view for readers.
    '''
    template_name = 'dashboards/reader.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(
            approved=True
        )
        return context


class EditorDashboardView(LoginRequiredMixin, TemplateView):
    '''
    Dashboard view for editors.
    '''
    template_name = 'dashboards/editor.html'


class JournalistDashboardView(LoginRequiredMixin, TemplateView):
    '''
    Dashboard view for Journalists.
    '''
    template_name = 'dashboards/journalist.html'


class EntryPointView(View):
    '''
    A simple entry point view to test authentication.
    '''
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard-redirect')
        return redirect('login')
