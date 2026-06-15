from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, DriverRegistrationForm
from .models import User 
from wallets.models import Wallet 
from django.contrib.auth.views import LoginView
from django.urls import reverse




def signup_view(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)
            Wallet.objects.create(user=user, balance=0.00)


            return redirect('trips:trip-list')

    else:

        form = SignUpForm()

    return render( request, 'accounts/signup.html',  {'form': form},)

def logout_view(request):
    logout(request)
   
    return redirect('home')


def register_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            if user.role == 'DRIVER':
                return redirect('trips:driver-dashboard')
            return redirect('home')
    else:
        form = DriverRegistrationForm()
    return render(request, 'accounts/register-driver.html', {'form': form})



class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'DRIVER':
            if hasattr(user, 'driver_profile') and not user.driver_profile.is_approved:
                return reverse('trips:waiting-approval') 
            return reverse('trips:driver-dashboard')
        return reverse('home')