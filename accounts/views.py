from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignUpForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'home'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
