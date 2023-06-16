from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("chat.urls")),
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('admins/', include('Admin.urls')),
    path('doctor/', include('Doctors.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)