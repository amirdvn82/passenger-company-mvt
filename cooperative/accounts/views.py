from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, DriverRegistrationForm
from .models import User 
from wallets.models import Wallet 

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
   
    return redirect('/')


def register_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('/')
    else:
        form = DriverRegistrationForm()
    return render(request, 'accounts/register-driver.html', {'form': form})