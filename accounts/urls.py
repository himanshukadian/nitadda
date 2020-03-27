from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register/$', views.UserFormView.as_view(), name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'profile/$', views.profile, name='profile'),
    path('<int:pk>/update/', views.UserUpdateFormView.as_view(), name='update-profile'),

]
