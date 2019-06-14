from django.contrib import admin
from Questions.models import Question, Choice, Personal, Analisis

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Personal)
admin.site.register(Analisis)


