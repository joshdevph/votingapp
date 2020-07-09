from django.urls import path
from django.conf.urls import url
from . import views

namespace='admin_stockholder'

urlpatterns = [
    path('', views.admin_stockholder, name='admin_stockholder'),
    url(r'^update/(?P<pk>\d+)/$', views.update_stockholder, name='update_stockholder'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_stockholder, name='delete_stockholder'),
]