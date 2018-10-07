from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile


class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs = {'class':'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise ValidationError('User with this email already exists')
        return email

class RegistrationForm(forms.Form):
    username = forms.CharField(
                label = 'Username',
                max_length = 50,
                min_length = 2,
                widget = forms.TextInput(attrs = {'class':'form-control'})
                )
    email = forms.EmailField(
                label = 'Email',
                max_length = 100,
                widget = forms.TextInput(attrs = {'class':'form-control'})
                )
    password1 = forms.CharField(
                    label = 'Password',
                    max_length = 30,
                    min_length = 4,
                    widget = forms.PasswordInput(attrs = {'class':'form-control'})
                    )
    password2 = forms.CharField(
                    label = 'Confirm password',
                    max_length = 30,
                    min_length = 4,
                    widget = forms.PasswordInput(attrs = {'class':'form-control'})
                    )
    first_name = forms.CharField(
                    label = 'First name',
                    max_length = 50,
                    min_length = 1,
                    widget = forms.TextInput(attrs = {'class':'form-control'})
                    )
    last_name = forms.CharField(
                    label = 'Last name',
                    max_length = 50,
                    min_length = 1,
                    widget = forms.TextInput(attrs = {'class':'form-control'})
                    )

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise ValidationError('User with this email already exists')
        return email

    def clean_password(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2:
            if p1 != p2:
                raise ValidationError('Invalid password')


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
                'image' : forms.ClearableFileInput()
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['status']
        widgets = {
                'status' : forms.TextInput(attrs = {'class':'form-control'})
         }
