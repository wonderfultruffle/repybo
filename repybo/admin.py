from django.contrib import admin
from . import models

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["subject"]

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer)