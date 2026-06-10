from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):

    phone_number = forms.CharField(max_length=11)

    class Meta:

        model = User

        fields = ( 'username', 'phone_number', 'password1', 'password2',)