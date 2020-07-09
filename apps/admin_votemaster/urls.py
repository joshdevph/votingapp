from django.urls import path
from . import views

namespace = 'admin_votemaster'

urlpatterns = [
    path('', views.admin_votemaster, name='admin_votemaster'),
    path('attendance/', views.admin_votemaster_attendance, name='admin_votemaster_attendance'),
    path('nomination/', views.admin_votemaster_nomination, name='admin_votemaster_nomination'),
]