from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    
    # Auth endpoints
    path('auth/login/', views.login_view, name='api_login'),
    path('auth/logout/', views.logout_view, name='api_logout'),
    path('auth/check/', views.auth_check, name='api_auth_check'),
    
    # Data endpoints
    path('equipos/', views.listar_equipos, name='api_equipos'),
    path('reparaciones/', views.listar_reparaciones, name='api_reparaciones'),
    path('repuestos/', views.listar_repuestos, name='api_repuestos'),
]
