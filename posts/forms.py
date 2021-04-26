from django import forms
from django.utils.translation import gettext_lazy
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'group': gettext_lazy('Группа'),
            'text': gettext_lazy('Текст'),
            'image': gettext_lazy('Изображение')
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
