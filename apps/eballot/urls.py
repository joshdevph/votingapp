from django.urls import path
from . import views

namespace='eballot'

urlpatterns = [
    path('select_election/', views.select_election, name='select_election'),
    path('create_eballot/', views.create_eballot, name='create_eballot')
]