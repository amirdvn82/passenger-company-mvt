from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from accounts.views import CustomLoginView, logout_view

app_name = 'accounts'

urlpatterns = [

    path("signup/", signup_view, name="signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password-change.html', success_url=reverse_lazy('accounts:password-change-done')) , name='password-change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password-change-done.html'),  name='password-change-done'),
    path('register/driver/', register_driver, name='register-driver'),
    
    

]