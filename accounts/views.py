from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from accounts.services import generate_token, issue_jwt_token, issue_jwt_refresh_token


from .forms import CustomAuthenticationForm


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

@login_required
def token_generation_view(request):
    """Generates a token and displays it"""
    token = generate_token(request.user)
    jwt_token = issue_jwt_token(request.user)
    refresh_token = issue_jwt_refresh_token(request.user)
    return render(
        request, 'accounts/token_display.html',
        {
            "token": token, 
            "jwt_token": jwt_token, 
            "refresh_token": refresh_token
        }
    )
