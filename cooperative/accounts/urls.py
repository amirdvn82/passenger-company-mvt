from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [

    path("signup/", signup_view, name="signup"),
    path('register/driver/', register_driver, name='register-driver'),
    
    

]