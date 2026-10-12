
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, Http404
from django.views.static import serve as static_serve


def google_verify(request, token):
    """Google Search Console verifikatsiya fayllarini (google*.html) ildizdan xizmat qiladi."""
    path = settings.BASE_DIR / 'static' / f'google{token}.html'
    if not path.exists():
        raise Http404
    return FileResponse(open(path, 'rb'), content_type='text/html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', include('dashboard.urls')),
    path('google<str:token>.html', google_verify),
    path('', include('bot.urls')),
    path('', include('frontend.urls') )
]

# Yuklangan rasmlar (media) productionda ham xizmat qilinishi kerak.
# DEBUG=False bo'lganda Django static() helper media'ni bermaydi, shu sabab alohida.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path('webstorm/<path:path>', static_serve, {'document_root': settings.BASE_DIR / 'webstorm'}),
    ]
