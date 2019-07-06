from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Sorry, This Email is already taken!')
        return email

    class Meta:
        model = get_user_model()
        fields = ('username','email','password1','password2')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email',]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image',]
