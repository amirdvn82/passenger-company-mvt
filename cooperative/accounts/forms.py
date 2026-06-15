from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DriverProfile, Vehicle

class SignUpForm(UserCreationForm):

    phone_number = forms.CharField(max_length=11)

    class Meta:

        model = User

        fields = ( 'username', 'phone_number', 'password1', 'password2',)

class DriverRegistrationForm(UserCreationForm):
    national_code = forms.CharField(max_length=10, required=True, label= 'National Code' )
    license_number = forms.CharField(max_length=20, required=True, label='License Number ')
    plate_number = forms.CharField(max_length=15, required=True, label='Plate Number')
    car_model = forms.CharField(max_length=50, required=True, label='Car Model')
    capacity = forms.IntegerField(min_value=1, required=True, label='Capacity')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.role = User.Role.DRIVER
        if commit:
            user.save()

            driver_profile=DriverProfile.objects.create(
                user=user,
                national_code=self.cleaned_data['national_code'],
                license_number=self.cleaned_data['license_number'],
                is_approved=False  
            )
            Vehicle.objects.create(
                driver=driver_profile,
                plate_number=self.cleaned_data['plate_number'],
                car_model=self.cleaned_data['car_model'],
                capacity=self.cleaned_data['capacity']
            )
        return user