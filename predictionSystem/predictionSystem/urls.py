# stockprediction/urls.py

from django.conf.urls.static import static
from . import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
