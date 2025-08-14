from django import forms
from django.contrib.auth.forms import AuthenticationForm

from core.models import UserProfile


class StyledLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Password'
        })
    )

class UserProfileInlineForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['branch', 'department', 'role', 'phone']

    def clean_branch(self):
        branch = self.cleaned_data.get('branch')
        if not branch:
            raise forms.ValidationError("Branch is required.")
        return branch