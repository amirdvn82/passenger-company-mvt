"""
URL configuration for cooperative project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from trips.views import home_view
from django.urls import reverse_lazy
from accounts.views import CustomLoginView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_view, name='home'),
    path('tickets/', include('tickets.urls', namespace='tickets')),
    path('trips/', include('trips.urls', namespace='trips')),
    path('accounts', include('accounts.urls', namespace='accounts')),
    path('wallet/', include('wallets.urls', namespace='wallets')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password-change.html', success_url=reverse_lazy('password-change-done')) , name='password-change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password-change-done.html'),  name='password-change-done'),

]
