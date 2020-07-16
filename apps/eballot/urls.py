from django.urls import path
from . import views

namespace='eballot'

urlpatterns = [
    path('select_election/', views.select_election, name='select_election'),
    path('create_eballot/', views.create_eballot, name='create_eballot'),
    path('eballot_list/', views.eballot_list, name='eballot_list'),
    path('eballot_list/eballot_form/<int:id>', views.eballot_form, name='eballot_form'),
    path('eballot_list/eballot_form/cast_vote/<int:id>', views.cast_vote, name='cast_vote'),
    path('eballot_list/eballot_form/cast_remove/<int:id> <int:sh_id>', views.cast_remove, name='cast_remove'),
    path('result/', views.result, name='result'),
    path('result/update_elected/<str:id>', views.update_elected, name='update_elected')
]