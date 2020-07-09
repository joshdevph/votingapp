from django.urls import path
from . import views

namespace = 'admin_votemaster'

urlpatterns = [
    path('', views.admin_votemaster, name='admin_votemaster'),
    path('attendance/', views.admin_votemaster_attendance, name='admin_votemaster_attendance'),
    path('nomination/', views.admin_votemaster_nomination, name='admin_votemaster_nomination'),
    path('nomination/add_nominee/<int:id>', views.admin_votemaster_add_nominee, name='admin_votemaster_add_nominee'),
    path('nomination/delete_nominee/<int:id>', views.admin_votemaster_remove_nominee, name='admin_votemaster_remove_nominee'),
]