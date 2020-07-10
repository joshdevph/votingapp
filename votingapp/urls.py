
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('admin_dashboard/',include('apps.admin_dashboard.urls')),
    path('admin_stockholder/',include('apps.admin_newstockholder.urls')),
    path('admin_votemaster/',include('apps.admin_votemaster.urls')),
    # path('client_dashboard/',include('apps.clientdashboard.urls'))
    path('eballot/',include('apps.eballot.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

