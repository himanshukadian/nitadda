from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
from content.models import *
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
admin.site.register(Note)
admin.site.register(Note_Count)
admin.site.register(Course)
admin.site.register(College)
admin.site.register(Exam_Paper)
admin.site.register(Exam_Paper_Count)
admin.site.register(Book)
admin.site.register(Book_Count)
admin.site.register(Blog,BlogAdmin)
