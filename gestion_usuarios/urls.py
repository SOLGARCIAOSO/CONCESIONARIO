from django.urls import path
from . import views


urlpatterns = [
    path('home/' , views.listar_usuarios, name='home-usuarios'),
    path('roles/' , views.listar_roles, name='roles'),
    path('nuevo_usuario/', views.nuevo_usuario, name='nuevo_usuario'),
    path('permisos/', views.permisos, name='permisos'),
    path('editar_usuario/<int:usuario_id>/',views.editar_usuario,name='editar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]