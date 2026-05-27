from django import forms
from .models import Profile
from .models import Report
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'cs2_nickname',
            'rank',
            'primary_role',
            'secondary_role',
            'languages',
            'avatar',
        ]

class ReportForm(forms.ModelForm):

    class Meta:

        model = Report

        fields = ['reason']

class RegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]