from django.urls import path, include
from rest_framework import routers
from . import views
# from .views import MyViewSet  # ajusta según tus viewsets

router = routers.DefaultRouter()
# router.register(r'my', MyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('equipos/', views.listar_equipos, name='api_equipos'),
    path('reparaciones/', views.listar_reparaciones, name='api_reparaciones'),
    path('repuestos/', views.listar_repuestos, name='api_repuestos'),
    path('auth/login/', views.login_view, name='api_login'), 
]
