from django import forms
from rango.models import Category, Page


class CategoryForm(forms.ModelForm):
    # make slug a simple CharField and optional so the form doesn't reject submissions
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
