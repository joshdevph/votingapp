from django.urls import path
from . import views

namespace='client'

urlpatterns = [
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset/', views.reset, name='reset'),
    path('form/', views.complete_sh_data, name='complete_sh_data'),
    path('done/thankyou/', views.thank_you_form, name='thank_you_form'),
]