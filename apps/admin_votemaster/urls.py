from django.urls import path
from . import views

namespace = 'admin_votemaster'

urlpatterns = [
    path('', views.admin_votemaster, name='admin_votemaster'),
    path('edit/<int:id>', views.admin_votemaster_edit_election, name='admin_votemaster_edit_election'),
    path('attendance/<int:id>', views.admin_votemaster_attendance, name='admin_votemaster_attendance'),
    path('nomination/<int:id>', views.admin_votemaster_nomination, name='admin_votemaster_nomination'),
    path('nomination/add_nominee/<int:sh_id>/<int:election_id>', views.admin_votemaster_add_nominee, name='admin_votemaster_add_nominee'),
    path('nomination/delete_nominee/<int:id>/<int:election_id>', views.admin_votemaster_remove_nominee, name='admin_votemaster_remove_nominee'),
    path('delete_election/<int:id>', views.admin_votemaster_delete_election, name='admin_votemaster_delete_election'),
]