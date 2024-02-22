from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        return password2


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username and '@' not in username:
            raise ValidationError("Enter a valid email address.", code='invalid')

        # Authenticate the user with the custom backend
        user = authenticate(request=self.request, username=username, password=cleaned_data.get('password'), backend='voting.backends.EmailBackend')

        if user is None:
            raise ValidationError("Invalid email or password.", code='invalid_login')

        # Set the authenticated user on the form
        self.user_cache = user

        return cleaned_data
