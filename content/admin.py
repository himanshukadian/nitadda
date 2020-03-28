from django.contrib import admin

# Register your models here.
from content.models import *

admin.site.register(Note)
admin.site.register(Note_Count)
admin.site.register(Course)
admin.site.register(Book)
