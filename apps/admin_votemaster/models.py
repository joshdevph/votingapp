from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Election(models.Model):
    description = models.CharField(null=False, max_length=254)
    code = models.CharField(null=False, max_length=254)
    date_added = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    sh_id = models.CharField(null=False, max_length=255)
    election_code = models.CharField(null=False, max_length=255)
    sh_fullname = models.CharField(null=False, max_length=255)
    at_status = models.CharField(null=True, max_length=255)

class Nominee(models.Model):
    sh_id = models.CharField(null=False, max_length=255)
    election_code = models.CharField(null=False, max_length=255)
    sh_fullname = models.CharField(null=False, max_length=255)