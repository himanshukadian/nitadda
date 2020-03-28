from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from nitadda import settings
from search.views import SearchNoteView
from . import views

urlpatterns = [
                  url(r'^$', SearchNoteView.as_view(), name='search'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
