
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('dashboard.urls')),
    path('googlee7d19afb2238cb03.html', static_serve, {
        'path': 'googlee7d19afb2238cb03.html',
        'document_root': settings.BASE_DIR / 'static',
    }),
    path('', include('bot.urls')),
    path('', include('frontend.urls') )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path('webstorm/<path:path>', static_serve, {'document_root': settings.BASE_DIR / 'webstorm'}),
    ]
