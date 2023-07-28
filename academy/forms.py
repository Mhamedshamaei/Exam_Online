from django import forms
from accounts.models import *


class AcademyCreateForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = ('name', 'url',)

    def clean_url(self):
        data = self.cleaned_data
        if Academy.objects.filter(url=data['url']).exists():
            raise forms.ValidationError('url already exist')
        return data['url']


class AcademyImageForm(forms.ModelForm):
    class Meta:
        model = AcademyGallery
        fields = ('g_image',)


class AcademyUpdateForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = ('name', 'url', 'image',)
