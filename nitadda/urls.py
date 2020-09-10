"""nitadda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

import accounts

urlpatterns = [
                  url('admin/', admin.site.urls),
                  url(r'^', include(('accounts.urls', 'accounts'), namespace='accounts')),
                  url(r'^search/', include(('search.urls', 'search'), namespace='search')),
                  url(r'content/', include(('content.urls', 'content'), namespace='content')),
                  url('password-reset$',
                      accounts.views.PasswordResetView.as_view(template_name='account/password_reset.html'),
                      name='password_reset'),
                  url('password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                      accounts.views.PasswordResetConfirmView.as_view(
                          template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
                  url('password-reset/done/',
                      accounts.views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
                      name='password_reset_done'),
                  url('password-reset-complete/', accounts.views.PasswordResetCompleteView.as_view(
                      template_name='account/password_reset_complete.html'), name='password_reset_complete'),
                  url(r'^tinymce/', include('tinymce.urls'))
                  # url('auth/', include('social_django.urls', namespace='social')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
