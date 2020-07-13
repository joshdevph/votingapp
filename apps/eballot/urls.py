from django.urls import path
from . import views

namespace='eballot'

urlpatterns = [
    path('select_election/', views.select_election, name='select_election'),
    path('create_eballot/', views.create_eballot, name='create_eballot'),
    path('eballot_list/', views.eballot_list, name='eballot_list'),
    path('eballot_list/eballot_form/<int:id>', views.eballot_form, name='eballot_form'),
    path('eballot_list/eballot_form/save_vote/<int:id>', views.save_vote, name='save_vote')
]