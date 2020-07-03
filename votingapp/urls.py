
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('admin_dashboard/',include('apps.admin_dashboard.urls')),
    path('admin_stockholder/',include('apps.admin_newstockholder.urls')),
    path('client_dashboard/',include('apps.clientdashboard.urls'))
]
