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
from django.conf import settings
from django.conf.urls.static import static
from sigelin import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include('sigelin.urls_api')),
    
    # QR
    path('equipos/<uuid:pk>/qr/', views.ver_qr_equipo, name='ver_qr_equipo'),
    
    # Páginas del Frontend
    path('', views.index, name='index'),
    path('dashboard.html', views.dashboard, name='dashboard'),
    path('equipos.html', views.equipos, name='equipos'),
    path('reparaciones.html', views.reparaciones, name='reparaciones'),
    path('inventario.html', views.inventario, name='inventario'),
    path('reportes.html', views.reportes, name='reportes'),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

