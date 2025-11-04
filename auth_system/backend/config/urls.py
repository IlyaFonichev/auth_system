"""
URL configuration for auth_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from auth_system.backend.auth_app.views import (
    AuthViewSet, UserProfileViewSet, ProjectViewSet,
    DocumentViewSet, RoleViewSet, PermissionViewSet
)
from auth_system.backend.auth_app.views_web import RegisterView, LoginView, ProfileView, LogoutView

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'documents', DocumentViewSet, basename='documents')
router.register(r'admin/roles', RoleViewSet, basename='roles')
router.register(r'admin/permissions', PermissionViewSet, basename='permissions')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('', RedirectView.as_view(url='/profile/', permanent=False)),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
]
