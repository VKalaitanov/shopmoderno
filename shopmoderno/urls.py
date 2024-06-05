from django.contrib import admin
from django.urls import path, include
from shopmoderno import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('moderno.urls', namespace='moderno')),
    path('', include('cart.urls', namespace='cart')),
    path('', include('like.urls', namespace='like')),
    path('users/', include('users.urls', namespace='users')),
    path('order/', include('order.urls', namespace='order')),
    # path("__debug__/", include("debug_toolbar.urls")),
    path('social-auth/', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)