from django import forms
from rango.models import Category, Page
from django.contrib.auth.models import User
from rango.models import UserProfile


class CategoryForm(forms.ModelForm):
    slug = forms.CharField(required=False)

    class Meta:
        model = Category
        fields = ('name', 'views', 'likes', 'slug')


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
