from django.urls import path
from . import views

urlpatterns = [
    path('home/' , views.listar_usuarios, name='home-usuarios'),
    path('roles/' , views.listar_roles, name='roles')
]