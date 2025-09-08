from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.contrib import messages

def register(request):
    """ Register user """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect('login') # Register to the login page or any other page you want
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
