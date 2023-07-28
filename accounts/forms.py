from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
from django.contrib.auth import authenticate


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'email', 'national_code',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] and data['password1'] and data['password2'] != data['password1']:
            raise forms.ValidationError('passwords not same')
        return data['password2']

    def clean_national_code(self):
        data = self.cleaned_data
        if User.objects.filter(national_code=data['national_code']).exists():
            raise forms.ValidationError('national code already exist')
        return data['national_code']

    def clean_email(self):
        data = self.cleaned_data
        if User.objects.filter(email=data['email']).exists():
            raise forms.ValidationError('email already exist')
        return data['email']

    def clean_phone(self):
        data = self.cleaned_data
        if User.objects.filter(phone=data['phone']).exists():
            raise forms.ValidationError('phone already exist')
        return data['phone']

    def save(self, commit=True):
        data = self.cleaned_data
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ('email_phone', 'phone', 'email', 'national_code', 'role',)

    def clean_password(self):
        return self.initial['password']


class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = ('first_name', 'last_name', 'father_name','image',)


class OwnerUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'email', 'national_code',)


class StudentProfileForm(forms.ModelForm):
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


class UserLoginForm(forms.Form):
    email_phone = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

    def login(self, request):
        email_phone = self.cleaned_data.get('email_phone')
        password = self.cleaned_data.get('password')
        user = authenticate(email_phone=email_phone, password=password)
        return user


class ActiveCodeForm(forms.ModelForm):
    class Meta:
        model = ActiveCode
        fields = ('code',)

    def clean_code(self):
        code = self.cleaned_data['code']
        if len(str(code)) != 6:
            forms.ValidationError('code is invalid !')
        return code
