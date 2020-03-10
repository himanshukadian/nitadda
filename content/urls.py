from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('upload_note/', views.UploadNote, name='Upload_Note'),
    url(r'^shownote/(?P<probid>\w+)', views.Display_Note, name='Display_Note'),
    url(r'^deletenote/(?P<noteid>\w+)', views.Delete_Note, name='Delete_Note'),
    url('login/', views.admin_login, name='admin_login'),
    url('logout/', views.admin_logout, name='admin_logout'),
    url(r'^add_course$', views.Add_Course, name='Add_Course'),
    url(r'^course$', views.course_list, name='course_list'),
    url(r'^all_note$', views.Get_Note, name='Get_Note'),
    # url(r'^course/(?P<pk>\d+)/$', views.course_detail, name='course_detail'),
]
