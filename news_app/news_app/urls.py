"""
URL configuration for news_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth.views import LoginView, LogoutView
from users.views import RegisterView, EntryPointView

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT auth views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # authentication views
    path('login/', LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', EntryPointView.as_view(), name='home'),
    # app urls
    path('', include('users.urls')),
    path('', include('articles.urls')),
    path('', include('newsletters.urls')),
    path('', include('publishers.urls')),
    path('', include('subscriptions.urls')),
    # API endpoints
    path("api/", include("articles.api.urls")),
]
