"""
URL configuration for sigelin_project project.

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
from sigelin import views as sigelin_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('equipos/<uuid:pk>/qr/', sigelin_views.ver_qr_equipo, name='ver_qr_equipo'),
    path('admin/', admin.site.urls),
    path('api/', include('sigelin.urls_api')),  # tus endpoints DRF
    path('dashboard.html', sigelin_views.dashboard, name='dashboard'),
    # cualquier otra ruta que no sea /api/ caera al index de la SPA:
    re_path(r'^(?:.*)/?$', sigelin_views.index),
]
# servir media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

