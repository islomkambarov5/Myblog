from django import forms
from .models import Comments


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('user', 'email', 'body')
