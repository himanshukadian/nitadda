from django.contrib import admin

# Register your models here.
from content.models import *

admin.site.register(Note)
admin.site.register(Note_Count)
admin.site.register(Course)
admin.site.register(College)
admin.site.register(Exam_Paper)
admin.site.register(Exam_Paper_Count)
admin.site.register(Book)
admin.site.register(Book_Count)
admin.site.register(Blog)
