from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home-inventario'),
    path('inventario/', views.inventario, name='inventario'),
    path('vehiculos/crear/', views.crear_vehiculo, name='crear-vehiculo'),
    path('vehiculos/editar/<int:vehiculo_id>/', views.editar_vehiculo, name='editar-vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar-vehiculo'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear-cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar-cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar-cliente'),
    path('reservas/', views.reservas, name='reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear-reserva'),
    path('reservas/cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar-reserva'),
]
