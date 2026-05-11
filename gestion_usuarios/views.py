from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioForm
from . import models

def listar_usuarios(request):
    busqueda = request.GET.get('busqueda')
    lista_usuarios = models.Usuario.objects.all()

    if busqueda:
        lista_usuarios = lista_usuarios.filter(tercero__nombre__icontains=busqueda)

    return render(request, 'home.html', {'lista_usuarios': lista_usuarios})


def listar_roles(request):
    lista_roles = models.Rol.objects.all()

    data = {'lista_roles': lista_roles}
    return render(request, 'roles.html', data )


def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            tercero = models.Tercero.objects.create(
                nombre = formulario.cleaned_data['nombre'],
                tipo_documento = formulario.cleaned_data['tipo_documento'],
                numero_documento = formulario.cleaned_data['numero_documento'],
                telefono = formulario.cleaned_data['telefono'],
                direccion = formulario.cleaned_data['direccion'],
                email = formulario.cleaned_data['email']
            )

            models.Usuario.objects.create(
                tercero = tercero,
                rol = formulario.cleaned_data['rol'],
                contrasena = formulario.cleaned_data['contrasena'],
                habilitado = formulario.cleaned_data['habilitado']
            )

            messages.success(request, f'Usuario "{tercero.nombre}" registrado correctamente.')
            return redirect('/usuario/home/')
    else:
        formulario = UsuarioForm()

    return render(request, 'nuevo_usuario.html', {'formulario': formulario})


def editar_usuario(request, usuario_id):
    usuario = models.Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        usuario.tercero.nombre = request.POST['nombre']
        usuario.tercero.tipo_documento = request.POST['tipo_documento']
        usuario.tercero.numero_documento = request.POST['numero_documento']
        usuario.tercero.telefono = request.POST['telefono']
        usuario.tercero.direccion = request.POST['direccion']
        usuario.tercero.email = request.POST['email']
        usuario.tercero.save()

        usuario.rol = models.Rol.objects.get(id=request.POST['rol'])
        usuario.habilitado = 'habilitado' in request.POST
        usuario.cuenta_activa = 'cuenta_activa' in request.POST
        usuario.save()

        return redirect('/usuario/home/')

    data = {
        'usuario': usuario,
        'lista_roles': models.Rol.objects.all()
    }

    return render(request, 'editar_usuario.html', data)


def eliminar_usuario(request, usuario_id):
    usuario = models.Usuario.objects.get(id=usuario_id)
    usuario.delete()

    return redirect('/usuario/home/')


def permisos(request):
    return render(request, 'permisos.html')