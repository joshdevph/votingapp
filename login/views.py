from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from apps.admin_newstockholder.models import StockHolder

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Fetching data of Logged in user
            getusername = request.user.get_username()
            logged_user = User.objects.get(username=getusername)
            user_id = logged_user.id
            is_staff = logged_user.is_staff
            fname = logged_user.first_name
            lname = logged_user.last_name
            # Storing UserID and UserLevel (Adim or Client) to Session
            request.session['user_id'] = user_id
            request.session['is_staff'] = is_staff
            fullname = fname + ' ' + lname
            request.session['fullname'] = fname + ' ' + lname


            if is_staff == False:
                stockholder= StockHolder.objects.get(sh_account=user_id)

                status = stockholder.sh_password_status
                if status == "Updated":
                    return redirect('complete_sh_data')
                else:
                    # redirect to change password form
                    return redirect('reset_password')

            else:
                return redirect('admin_dashboard')
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