from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from nitadda import settings
from . import views

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^meetOurTeam/$', TemplateView.as_view(template_name='meet_our_team.html')),
                  url(r'^upvote/$', views.Upvote),
                  url('upload/', views.UploadNote, name='Upload_Note'),
                  url('approvenote/(?P<noteid>\w+)', views.Approve_Note, name='Approve_Note'),
                  url(r'^deletenote/(?P<noteid>\w+)', views.Delete_Note, name='Delete_Note'),
                  url(r'^view/(?P<noteid>\w+)', views.Display_Pdf, name='Display_Pdf'),
                  url(r'^course_notes/(?P<slug>[-\w]+)/$', views.Show_Note, name='Course_Note'),
                  url(r'^subject_notes/(?P<slug>[-\w]+)/$', views.Show_Subject_Note, name='Subject_Note'),
                  url(r'getSubjects/', views.getSubjects),
                  url('login/', views.admin_login, name='admin_login'),
                  url('logout/', views.admin_logout, name='admin_logout'),
                  url(r'^add_course$', views.Add_Course, name='Add_Course'),
                  url(r'^add_subject$', views.Add_Subject, name='Add_Subject'),
                  url(r'^course$', views.course_list, name='course_list'),
                  url(r'^all_subject_note$', views.Get_Subject_Note, name='Get_Subject_Note'),
                  url(r'^all_course$', views.Get_Course, name='Get_Course'),
                  url(r'^all_subject$', views.Get_Subject, name='Get_Subject'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
