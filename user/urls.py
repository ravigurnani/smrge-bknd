"""smrge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('register', register_user),
    path('gen_otp', generate_otp),
    path('gen_otp_extra', generate_otp_extra),
    path('verify_otp', verify_otp),
    path('verify_otp_extra', verify_otp_extra),
    path('update_profile', update_profile),
    path('get_profiles', get_profiles),
    path('get_token', get_token),
    path('get_user_profile', get_user_profile),
    path('add_smrge', save_profile),
    path('remove_smrge', remove_profile),
    path('get_all_interests', get_all_interests),
    path('get_saved_profiles', get_saved_profiles),
    path('google_verification', google_verification)
]
