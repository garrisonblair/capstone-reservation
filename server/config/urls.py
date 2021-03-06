from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path(r'', include('apps.accounts.urls')),
    path(r'', include('apps.booking.urls')),
    path(r'', include('apps.system_administration.urls')),
    path(r'', include('apps.rooms.urls')),
    path(r'', include('apps.groups.urls')),
    path(r'', include('apps.statistics.urls')),
    path(r'', include('apps.card_reader.urls')),
    path(r'', include('apps.notifications.urls')),
    path(r'', include('apps.booker_settings.urls')),
    path(r'', include('apps.csv.urls')),
    path('admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'', include_docs_urls(title='Capstone'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
