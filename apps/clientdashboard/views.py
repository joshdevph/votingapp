from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.




@login_required(login_url="")
def reset_password(request):
    return render(request, 'reset_password.html')
