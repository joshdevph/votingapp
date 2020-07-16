from django.urls import path
from . import views

namespace = 'login'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
