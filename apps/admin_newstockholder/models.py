from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StockHolder(models.Model):
    sh_fname = models.CharField(null=False, max_length=254)
    sh_lname = models.CharField(null=False, max_length=254)
    sh_mname = models.CharField(blank=True, max_length=254)
    sh_email = models.CharField(null=False, max_length=254)
    sh_position = models.CharField(blank=True, max_length=254)
    company_images = models.ImageField(upload_to='Media_Files/StockHolder_Profile_Picture', blank=True, default='static/images/user.png')
    sh_proxy_fname = models.CharField(blank=True, max_length=254)
    sh_proxy_lname = models.CharField(blank=True, max_length=254)
    sh_proxy_mname = models.CharField(blank=True, max_length=254)
    sh_date_added = models.DateTimeField(auto_now_add=True)
    sh_account= models.ForeignKey(User, null=False, on_delete=models.CASCADE)