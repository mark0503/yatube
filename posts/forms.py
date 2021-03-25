from django import forms
from django.utils.translation import gettext_lazy
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text')
        labels = {
           'group': gettext_lazy('Группа'),
           'text': gettext_lazy('Текст')
        }
