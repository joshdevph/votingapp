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
    path('eballot_list/eballot_form/vote_summary/<str:id>', views.vote_summary, name='vote_summary'),
    path('result/', views.result, name='result'),
    path('result/end_election/<str:id>', views.end_election, name='end_election'),
    path('result/update_elected/<str:id>', views.update_elected, name='update_elected'),
    path('select_election_report/', views.select_election_report, name='select_election_report'),
    path('select_election_report/voters_list/<str:id>', views.voters_list, name='voters_list'),
    path('vote_history/', views.vote_history, name='vote_history'),
    path('vote_history/history_details/<str:id>', views.history_details, name='history_details')

]