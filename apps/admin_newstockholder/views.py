from django.shortcuts import render, redirect
from apps.admin_newstockholder.forms import UserForm
from .models import StockHolder
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from apps.clientdashboard.forms import AccountForm
from django.core.files.storage import FileSystemStorage
import datetime
from django.contrib import messages
# Create your views here.

def admin_stockholder(request):
    sh_list =  StockHolder.objects.all().exclude(sh_account_status='deleted')
    user_form = UserForm(request.POST)
    form = AccountForm(request.POST, request.FILES)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        form = AccountForm(request.POST, request.FILES)
        if user_form.is_valid()and form.is_valid():
            # Save User Credentials
            user = user_form.save()
            random_password = get_random_string(length=12)
            hashed_pass = make_password(random_password)
            user.password = hashed_pass
            user.save()
            account_user = user.id
    
            sh_fname = request.POST.get("sh_fname")
            sh_lname = request.POST.get("sh_lname")
            sh_mname = request.POST.get("sh_mname")
            sh_email = request.POST.get("sh_email")
            sh_position = request.POST.get("sh_position")
            upload_images = request.FILES['company_images']
            sh_proxy_fname = request.POST.get("sh_proxy_fname")
            sh_proxy_lname = request.POST.get("sh_proxy_lname")
            sh_proxy_mname = request.POST.get("sh_proxy_mname")

            if upload_images:
                fs = FileSystemStorage()
                current_datetime = datetime.datetime.now()
                date = str(current_datetime.month)+'-'+str(current_datetime.day)+'-'+str(current_datetime.year)
                time = str(current_datetime.hour)+str(current_datetime.minute)+str(current_datetime.second)
                # comp_code = company_data.company_code
                ext = upload_images.name.split(".")[-1]
                name = fs.save('Media_Files/StockHolder_Profile_Picture/'+time+'.'+ext, upload_images)
                url = fs.url(name)

            sh = StockHolder.objects.create(sh_fname=sh_fname, 
                                            sh_lname=sh_lname,
                                            sh_mname=sh_mname,
                                            sh_email=sh_email,
                                            sh_position=sh_position,
                                            company_images=url,
                                            sh_proxy_fname=sh_proxy_fname,
                                            sh_proxy_lname=sh_proxy_lname,
                                            sh_proxy_mname=sh_proxy_mname,
                                            sh_account= User.objects.get(id=account_user),
                                            )

    else:
        form = AccountForm()
        user_form = UserForm()
    return render(request, 'admin/content/admin_stockholder.html', {'form': form, 'sh_list' : sh_list, 'user_form': user_form,})

def update_stockholder(request, pk):
    if request.method == "POST":
        sh_fname = request.POST.get("sh_fname")
        sh_lname = request.POST.get("sh_lname")
        sh_mname = request.POST.get("sh_mname")
        sh_email = request.POST.get("sh_email")
        sh_position = request.POST.get("sh_position")
        upload_images = request.FILES['company_images']
        sh_proxy_fname = request.POST.get("sh_proxy_fname")
        sh_proxy_lname = request.POST.get("sh_proxy_lname")
        sh_proxy_mname = request.POST.get("sh_proxy_mname")

        # UPLOAD IMAGE IN MEDIA STORAGE and CONVERTING ITS FILENAME
        if upload_images:
                fs = FileSystemStorage()
                current_datetime = datetime.datetime.now()
                date = str(current_datetime.month)+'-'+str(current_datetime.day)+'-'+str(current_datetime.year)
                time = str(current_datetime.hour)+str(current_datetime.minute)+str(current_datetime.second)
                ext = upload_images.name.split(".")[-1]
                name = fs.save('Media_Files/StockHolder_Profile_Picture/'+time+'.'+ext, upload_images)
                url = fs.url(name)

        # SAVING STOCKHOLDER INFO
        sh_accounts = StockHolder.objects.filter(id=pk).update(sh_fname=sh_fname,
                            sh_lname=sh_lname, 
                            sh_mname=sh_mname, 
                            sh_position=sh_position, 
                            company_images=url,
                            sh_proxy_fname=sh_proxy_fname, 
                            sh_proxy_lname=sh_proxy_lname, 
                            sh_proxy_mname=sh_proxy_mname)


    return redirect('admin_stockholder')

def delete_stockholder(request, pk):
    delete_sh = StockHolder.objects.filter(id=pk).update(sh_account_status='deleted')
    messages.error(request, 'Data Successfully Deleted')
    return redirect('admin_stockholder')
