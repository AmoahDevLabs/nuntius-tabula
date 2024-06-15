"""
URL configuration for messenger project.
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from users.views import profile

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('users.urls', namespace='users')),
    path('@<username>/', profile, name='profile'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
               static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Nuntius Tabula Admin'
admin.site.site_title = 'Nuntius Tabula Admin'
admin.site.index_title = 'Welcome to Nuntius Tabula Admin'
