from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'accounts/signup.html', param)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return redirect(to='/accounts/user/')

    else:
        form = LoginForm()

    param = {
        'form': form,
    }

    return render(request, 'accounts/login.html', param)

def logout_view(request):
    logout(request)

    return redirect(to='home') 

@login_required
def user_view(request):
    user = request.user

    params = {
        'user': user
    }

    return render(request, 'accounts/info.html', params)

def other_view(request):
    pass