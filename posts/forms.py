from django import forms
from .models import Post, Comment, Image


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Post
        fields = ['content', 'image']


class CommentModelForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'add a comment...'}))

    class Meta:
        model = Comment
        fields = ['content', ]

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('content','file',)
