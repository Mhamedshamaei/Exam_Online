from django import forms
from .models import *


class ExamCreateForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('name', 'description',)


class ExamUpdateForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('name', 'description', 'time', 'start_time', 'start_date', 'end_time', 'end_date', 'negative',)


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = TQuestion
        fields = ('text', 'level',)


class ChoiceCreateForm(forms.ModelForm):
    class Meta:
        model = Choices
        fields = ('text',)


class TQuestionUpdateForm(forms.ModelForm):
    class Meta:
        model = TQuestion
        fields = ('text', 'image', 'level', 'true', 'is_left')


class DQuestionUpdateForm(forms.ModelForm):
    class Meta:
        model = DQuestion
        fields = ('text', 'image', 'level', 'is_left')
