from django.urls import path
from .views import (
    RoleRedirectView, ReaderDashboardView,
    JournalistDashboardView, EditorDashboardView,
)


urlpatterns = [
    path('dashboard/', RoleRedirectView.as_view(), name='dashboard-redirect'),
    path('dashboard/reader/', ReaderDashboardView.as_view(),
         name='reader-dashboard'),
    path('dashboard/journalist/', JournalistDashboardView.as_view(),
         name='journalist-dashboard'),
    path('dashboard/editor/', EditorDashboardView.as_view(),
         name='editor-dashboard'),
]
