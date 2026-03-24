from django.urls import path
from . import views

urlpatterns = [
    path('home/' , views.listar_usuarios, name='home'),
    path('roles/' , views.listar_roles, name='roles')
]