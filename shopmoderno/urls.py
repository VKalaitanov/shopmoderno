from django.contrib import admin
from django.urls import path, include
from shopmoderno import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('moderno.urls', namespace='moderno')),
    path('', include('basket.urls', namespace='basket')),
    path('', include('like.urls', namespace='like')),
    path('users/', include('users.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)