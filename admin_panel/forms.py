from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

class BlogTagForm(forms.ModelForm):
    class Meta:
        model = BlogTags
        fields = '__all__'