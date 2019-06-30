from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    text    = forms.CharField(widget=forms.TextInput(attrs={'rows': '3'}))
    class Meta:
        model = Comment
        fields=('text',)