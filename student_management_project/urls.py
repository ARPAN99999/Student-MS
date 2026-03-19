"""
URL configuration for student_management_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404
from django.shortcuts import redirect
import re


LEGACY_STATIC_CDN_MAP = {
    'jquery/jquery.min.js': 'https://code.jquery.com/jquery-3.6.0.min.js',
    'jquery-ui/jquery-ui.min.js': 'https://code.jquery.com/ui/1.13.2/jquery-ui.min.js',
    'bootstrap/js/bootstrap.bundle.min.js': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js',
    'chart.js/Chart.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js',
    'moment/moment.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.4/moment.min.js',
    'daterangepicker/daterangepicker.js': 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-daterangepicker/3.1/daterangepicker.min.js',
    'tempusdominus-bootstrap-4/js/tempusdominus-bootstrap-4.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.39.0/js/tempusdominus-bootstrap-4.min.js',
    'tempusdominus-bootstrap-4/css/tempusdominus-bootstrap-4.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.39.0/css/tempusdominus-bootstrap-4.min.css',
    'overlayScrollbars/js/jquery.overlayScrollbars.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/overlayscrollbars/1.13.1/js/jquery.overlayScrollbars.min.js',
    'overlayScrollbars/css/OverlayScrollbars.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/overlayscrollbars/1.13.1/css/OverlayScrollbars.min.css',
    'summernote/summernote-bs4.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.20/summernote-bs4.min.js',
    'summernote/summernote-bs4.css': 'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.20/summernote-bs4.min.css',
    'jqvmap/jquery.vmap.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/jqvmap/1.5.1/jquery.vmap.min.js',
    'jqvmap/maps/jquery.vmap.usa.js': 'https://cdnjs.cloudflare.com/ajax/libs/jqvmap/1.5.1/maps/jquery.vmap.usa.js',
    'sparklines/sparkline.js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery-sparklines/2.1.2/jquery.sparkline.min.js',
    'jquery-knob/jquery.knob.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/jquery-knob/1.2.13/jquery.knob.min.js',
    'dist/js/adminlte.js': 'https://cdnjs.cloudflare.com/ajax/libs/admin-lte/3.2.0/js/adminlte.min.js',
    'dist/js/demo.js': 'https://cdnjs.cloudflare.com/ajax/libs/admin-lte/3.2.0/js/demo.js',
    'dist/js/pages/dashboard.js': 'https://cdnjs.cloudflare.com/ajax/libs/admin-lte/3.2.0/js/pages/dashboard.js',
    'dist/css/adminlte.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/admin-lte/3.2.0/css/adminlte.min.css',
    'fontawesome-free/css/all.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
}


def legacy_static_fallback(request, asset_path):
    target = LEGACY_STATIC_CDN_MAP.get(asset_path)
    if not target:
        raise Http404('Static asset not found')
    return redirect(target, permanent=False)


LEGACY_STATIC_PATTERN = '|'.join(re.escape(path) for path in LEGACY_STATIC_CDN_MAP.keys())

urlpatterns = [
    re_path(rf'^static/(?P<asset_path>{LEGACY_STATIC_PATTERN})$', legacy_static_fallback),
    path('admin/blogs/post/', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/blogs/post', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('student_management_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
