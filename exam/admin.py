from django.contrib import admin
from .models import *


class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'create', 'active',)


class TQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'level', 'true',)


class DQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'level',)


admin.site.register(Exam, ExamAdmin)
admin.site.register(TQuestion, TQuestionAdmin)
admin.site.register(DQuestion, DQuestionAdmin)
admin.site.register(Choices)
admin.site.register(AnswerSheet)
admin.site.register(Answer)
admin.site.register(GrowthChart)
