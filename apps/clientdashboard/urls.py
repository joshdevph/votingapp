from django.urls import path
from . import views

namespace='client'

urlpatterns = [
    path('reset-password', views.reset_password, name='reset_password'),
]