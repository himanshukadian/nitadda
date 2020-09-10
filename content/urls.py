from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from nitadda import settings
from . import views
from .views import *

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^meetOurTeam/$', TemplateView.as_view(template_name='meet_our_team.html')),
                  url(r'^upvote/$', views.Upvote),
                  url(r'^show_full_blog/(?P<blog_id>\w+)', views.show_full_blog),
                  url(r'^course_notes/(?P<slug>[-\w]+)/$', views.Show_Note, name='Course_Note'),
#                   url(r'^course_notes/(?P<slug>[-\w]+)/listing/', NoteTableData.as_view(), name='listing'),
                   # path('listing/', NoteTableData.as_view(), name='listing'),
                  url(r'^report/(?P<note_id>\w+)', views.report_post),
                  url('upload/', views.UploadContent, name='Upload_Content'),
                  # url('upload_note/', views.UploadNote, name='Upload_Note'),
                  # url('upload_paper/', views.UploadPaper, name='Upload_Paper'),
                  url('approvenote/(?P<noteid>\w+)', views.Approve_Note, name='Approve_Note'),
                  url('approvepaper/(?P<paperid>\w+)', views.Approve_Paper, name='Approve_Paper'),
                  url(r'^deletenote/(?P<noteid>\w+)', views.Delete_Note, name='Delete_Note'),
                  url(r'^deletepaper/(?P<paperid>\w+)', views.Delete_Paper, name='Delete_Paper'),
                  url(r'^view/(?P<noteid>\w+)', views.Display_Pdf, name='Display_Pdf'),
                  url(r'^view_paper/(?P<paperid>\w+)', views.Display_Paper_Pdf, name='Display_Paper_Pdf'),
                  url(r'^course_notes/(?P<slug>[-\w]+)/$', views.Show_Note, name='Course_Note'),
                  url(r'^subject_notes/(?P<slug>[-\w]+)/$', views.Show_Subject_Note, name='Subject_Note'),
                  url(r'getSubjects/', views.getSubjects),
                  url(r'getCourseDuration/', views.getCourseDuration),
                  url('login/', views.admin_login, name='admin_login'),
                  url('logout/', views.admin_logout, name='admin_logout'),
                  url(r'^add_course$', views.Add_Course, name='Add_Course'),
                  url(r'^add_subject$', views.Add_Subject, name='Add_Subject'),
                  url(r'^course$', views.course_list, name='course_list'),
                  url(r'^all_subject_note$', views.Get_Subject_Note, name='Get_Subject_Note'),
                  url(r'^all_course$', views.Get_Course, name='Get_Course'),
                  url(r'^all_subject$', views.Get_Subject, name='Get_Subject'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
