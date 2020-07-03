from django.shortcuts import render, redirect
from apps.admin_newstockholder.forms import UserForm
from .models import StockHolder
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# Create your views here.

def admin_stockholder(request):
    sh_list =  StockHolder.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            random_password = get_random_string(length=12)
            print(random_password)
            hashed_pass = make_password(random_password)
            user = form.save()
            user.password = hashed_pass
            user.save()
            uname= form['username'].value()
            fname= form['first_name'].value()
            lname= form['last_name'].value()
            email= form['email'].value()

            stockholder = StockHolder.objects.create(sh_fname=fname, sh_lname=lname, sh_email=email, sh_account=User.objects.get(password=hashed_pass))
            #Sending Email
            subject = 'User Access'
            message = 'Password :' + random_password + ' ' + 'Username :' + uname
            email_from = settings.EMAIL_HOST_USER
            recipient_list =[email]
            send_mail( subject, message, email_from, recipient_list )



    else:
        form = UserForm()
    return render(request, 'admin/content/admin_stockholder.html', {'form': form, 'sh_list' : sh_list,})
