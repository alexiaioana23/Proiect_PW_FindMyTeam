from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('teams/', include('teams.urls')),
    path('messages/', include('messages_app.urls')),
    path('announcements/', include('announcements.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)