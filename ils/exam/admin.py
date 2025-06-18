# Register your models here.

from django.contrib import admin
from .models import Question, Option, UserResponse

# Register your models here
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserResponse)
