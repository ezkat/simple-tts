from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
]


if not settings.DEBUG:
    urlpatterns.extend([
        re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ])
