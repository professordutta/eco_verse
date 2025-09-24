from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SignUpForm, ProfileUpdateForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

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

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('settings')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/settings.html', {'form': form})
