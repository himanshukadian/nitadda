from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'register/$', views.UserFormView.as_view(), name='register'),
    url(r'login/$', views.user_login, name='login'),
    url('logout/', views.admin_logout, name='admin_logout'),
    url(r'profile/$', views.profile, name='profile'),
    path('<int:pk>/update/', views.UserUpdateFormView.as_view(), name='update-profile'),
    url(r'contact_us/$', views.Contact_Us, name='contact_us'),
    url(r'inbox/$', views.Inbox, name='inbox'),
    url(r'inbox/show_message/$', views.Show_Message, name='show_message'),
    url(r'^inbox/mark_as_read/$', views.Mark_As_Read, name='mark_as_read'),
    url(r'^inbox/delete_message/$', views.Delete_Message, name='delete_message'),
    path('<int:pk>/clear/', views.clear, name='clear-noti'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
