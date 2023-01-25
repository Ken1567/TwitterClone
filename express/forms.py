import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'required': 'required'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if not re.match(r'^.{8,}$', password):
                raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Invalid username.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        user = authenticate(username=self.cleaned_data.get('username'), password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Invalid password.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, max_length=500, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'image']