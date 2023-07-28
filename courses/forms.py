from django import forms
from accounts.models import *


class CoursesCreateForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = ('name',)


class AddJsDic(forms.Form):
    dic = forms.CharField(max_length=1000)
