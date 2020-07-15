from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StockHolder(models.Model):
    sh_shares = models.CharField(null=False, max_length=254)
    mobile_no = models.CharField(null=False, max_length=254)
    sh_fname = models.CharField(null=False, max_length=254)
    sh_lname = models.CharField(null=False, max_length=254)
    sh_mname = models.CharField(blank=True, max_length=254)
    sh_email = models.CharField(null=False, max_length=254)
    sh_position = models.CharField(blank=True, max_length=254)
    company_images = models.FileField(upload_to='Media_Files/StockHolder_Profile_Picture')
    sh_proxy_fname = models.CharField(blank=True, max_length=254)
    sh_proxy_lname = models.CharField(blank=True, max_length=254)
    sh_proxy_mname = models.CharField(blank=True, max_length=254)
    sh_proxy_email = models.CharField(blank=True, max_length=254)
    sh_date_added = models.DateTimeField(auto_now_add=True)
    sh_account= models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    sh_password_status = models.CharField(blank=True, max_length=254)
    sh_account_status = models.CharField(blank=True, max_length=254)
    sh_proxy_status = models.BooleanField(default=False)
    sh_classification = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(blank=True, max_length=254)