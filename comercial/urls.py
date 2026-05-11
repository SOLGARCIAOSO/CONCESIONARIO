from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  
    path('lista_cotizaciones/', views.lista_cotizaciones, name='lista_cotizaciones'),
    path('lista_reservas/', views.lista_reservas, name='lista_reservas'),
    path('lista_ventas/', views.lista_ventas, name='lista_ventas'),
    path('crear_cotizacion/',views.crear_cotizacion, name='crear_cotizacion'),
    path('crear_reserva/',views.crear_reserva,name='crear_reserva'),
    path('crear_venta/',views.crear_venta,name='crear_venta'),
]


