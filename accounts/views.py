from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

# Create your views here.

User = get_user_model()

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
