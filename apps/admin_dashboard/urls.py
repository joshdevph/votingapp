from django.urls import path
from . import views

namespace='admin_dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard')
]