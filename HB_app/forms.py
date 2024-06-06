from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, DateField, EmailField


class RegistrationForm(UserCreationForm):
    first_name = CharField(max_length=20, required=True)
    last_name = CharField(max_length=20, required=True)
    email = EmailField(max_length=50, required=True)
    date_of_birth = DateField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class NotificationSettingsForm(forms.Form):
    notification_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
