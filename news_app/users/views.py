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
    """View to handle user registration.

        :model: User model for registration.
        :form_class: UserRegistrationForm for user input.
        :template_name: Template for rendering the registration form.
        :success_url: URL to redirect to upon successful registration.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Override form_valid to assign user to a group based on role.

        :param form: The validated form instance.
        :return: HTTP response redirecting to success_url.
        """
        response = super().form_valid(form)
        role = form.cleaned_data.get('role')

        group = Group.objects.get(name=role.capitalize())
        self.object.groups.add(group)

        return response


class RoleRedirectView(View):
    """View to redirect users based on their role after login.

        :get: Handles GET requests to redirect users.
        :param request: The HTTP request object.
        :return: HTTP response redirecting to the appropriate dashboard.
    """

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
    """A view for the reader's dashboard.

        :template_name: The template for the reader dashboard.
        :get_context_data: Method to add approved articles to the context.
    """
    template_name = 'dashboards/reader.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(
            approved=True
        )
        return context


class EditorDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view for Editors.

        :template_name: Template for the editor dashboard.
    """
    template_name = 'dashboards/editor.html'


class JournalistDashboardView(LoginRequiredMixin, TemplateView):
    """Docstring for JournalistDashboardView

        :template_name: Template for the journalist dashboard.
    """
    template_name = 'dashboards/journalist.html'


class EntryPointView(View):
    """
    View to redirect users to appropriate page based on authentication status.

        :get: Handles GET requests to redirect users.
        :param request: The HTTP request object.
        :return: HTTP response redirecting to dashboard or login page.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard-redirect')
        return redirect('login')
