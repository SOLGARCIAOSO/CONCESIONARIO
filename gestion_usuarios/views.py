from django.shortcuts import render
from django.http import HttpResponse
from . import models


def listar_usuarios(request):
    lista_usuarios = models.Usuario.objects.all()

    data = {'lista_usuarios': lista_usuarios}
    return render(request, 'home.html', data)

def listar_roles(request):
    lista_roles = models.Rol.objects.all()

    data = {'lista_roles': lista_roles}
    return render(request, 'roles.html', data )