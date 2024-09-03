# forms.py
from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        })
        ,label='Password:'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        })
        ,label='Confirm password:'
    )
    profilePicture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
        })
        ,label='Profile Picture:'
    )
    class Meta:
        model = User
        fields = ['username', 'mail', 'profilePicture']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'label': 'Username'
            }),
            'mail': forms.EmailInput(attrs={
                'class': 'form-control',
                'label': 'Mail'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
