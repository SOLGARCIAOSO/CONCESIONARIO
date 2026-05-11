from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include('gestion_usuarios.urls')),
    path('clientes-inventario/', include('clientes_inventario.urls')),
    path('comercial/', include('comercial.urls')),
  
]
