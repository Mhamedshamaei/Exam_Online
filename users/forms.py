from django import forms
from accounts.models import *


class FLProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('first_name', 'last_name',)


class StudentCodeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('national_code',)


class TeacherCodeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('national_code', 'phone')
