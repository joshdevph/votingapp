from django.urls import path
from . import views

namespace='admin_stockholder'

urlpatterns = [
    path('stockholder/', views.admin_stockholder, name='admin_stockholder'),
]