from django import forms
from accounts.models import *


class TeacherLoginForm(forms.Form):
    email_phone = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
