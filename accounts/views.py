from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.forms import UserRegistrationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages

# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
            else:
                messages.error(request, 'INVALID username or password')
            
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect('/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
    

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('/')
        else:
            form = UserRegistrationForm()

        context = {'form': form}
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('/')
    


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = '/accounts/password_reset_done/' 

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = '/accounts/reset_done/'