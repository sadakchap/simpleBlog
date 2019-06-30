from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    text    = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}))
    class Meta:
        model = Comment
        fields=('text',)

class EmailPostForm(forms.Form):
    name    = forms.CharField(max_length=255)
    email   = forms.EmailField()
    to      = forms.EmailField()
    comment= forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':'3'}))