from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DriverProfile

class SignUpForm(UserCreationForm):

    phone_number = forms.CharField(max_length=11)

    class Meta:

        model = User

        fields = ( 'username', 'phone_number', 'password1', 'password2',)

class DriverRegistrationForm(UserCreationForm):
    national_code = forms.CharField(max_length=10, required=True, label= 'national_code' )
    license_number = forms.CharField(max_length=20, required=True, label='license_number ')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.role = User.Role.DRIVER
        if commit:
            user.save()
            DriverProfile.objects.create(
                user=user,
                national_code=self.cleaned_data['national_code'],
                license_number=self.cleaned_data['license_number'],
                is_approved=False  
            )
        return user