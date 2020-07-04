from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from apps.admin_newstockholder.models import StockHolder
from .forms import AccountForm
from django.core.files.storage import FileSystemStorage
import datetime
# Create your views here.




@login_required(login_url="")
def reset_password(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    return render(request, 'reset_password.html')

def reset(request):
    user_id = request.session['user_id']
    
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        new_pass = request.POST.get('new_pass')
        hashed_pass = make_password(new_pass, None, 'pbkdf2_sha256')
        user.password = hashed_pass
        user.save()
        password_status = StockHolder.objects.filter(sh_account=user_id).update(sh_password_status="Updated")
        return redirect('login')
    else:
        return render(request, 'reset_password.html')
    return render(request, 'reset_password.html')


def complete_sh_data(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            sh_fname = form.cleaned_data.get("sh_fname")
            sh_lname = form.cleaned_data.get("sh_lname")
            sh_mname = form.cleaned_data.get("sh_mname")
            sh_email = form.cleaned_data.get("sh_email")
            sh_position = form.cleaned_data.get("sh_position")
            company_images = request.FILES['company_images']
            sh_proxy_fname = form.cleaned_data.get("sh_proxy_fname")
            sh_proxy_lname = form.cleaned_data.get("sh_proxy_lname")
            sh_proxy_mname = form.cleaned_data.get("sh_proxy_mname")

            if company_images:
                fs = FileSystemStorage()
                current_datetime = datetime.datetime.now()
                date = str(current_datetime.month)+'-'+str(current_datetime.day)+'-'+str(current_datetime.year)
                time = str(current_datetime.hour)+str(current_datetime.minute)+str(current_datetime.second)
                # comp_code = company_data.company_code
                ext = company_images.name.split(".")[-1]
                name = fs.save('Media_Files/Company_Profile_Picture/-['+date+']-['+time+'].'+ext, company_images)
                url = fs.url(name)

            sh = StockHolder.objects.filter(sh_account=user_id).update(sh_fname=sh_fname, 
                                            sh_lname=sh_lname,
                                            sh_mname=sh_mname,
                                            sh_email=sh_email,
                                            sh_position=sh_position,
                                            company_images=url,
                                            sh_proxy_fname=sh_proxy_fname,
                                            sh_proxy_lname=sh_proxy_lname,
                                            sh_proxy_mname=sh_proxy_mname,
                                            )
            return redirect('thank_you_form')
    else:
        form = AccountForm()
        form.fields['sh_fname'].widget.attrs['class'] = "form-control"
        form.fields['sh_lname'].widget.attrs['class'] = "form-control"
        form.fields['sh_mname'].widget.attrs['class'] = "form-control"
        form.fields['sh_email'].widget.attrs['class'] = "form-control"
        form.fields['sh_position'].widget.attrs['class'] = "form-control"
        form.fields['company_images'].widget.attrs['class'] = "form-control"
        form.fields['sh_proxy_fname'].widget.attrs['class'] = "form-control"
        form.fields['sh_proxy_lname'].widget.attrs['class'] = "form-control"
        form.fields['sh_proxy_mname'].widget.attrs['class'] = "form-control"

    return render(request, 'client/content/client_form.html', {'form' : form})

def thank_you_form(request):
    return render(request, 'client/content/thank_you.html')