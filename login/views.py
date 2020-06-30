from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect ('admin_dashboard')
        else:
            print('Invalid')
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs['id'] = "exampleInputEmail1"
        form.fields['password'].widget.attrs['id'] = "exampleInputPassword1"
    return render(request, 'login.html', { 'form' : form })

@login_required(login_url="")
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('login')