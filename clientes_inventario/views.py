from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from . import models


def home(request):
    total_clientes = models.Cliente.objects.count()
    total_vehiculos = models.Vehiculo.objects.count()
    total_reservas = models.Reserva.objects.filter(activa=True).count()
    vehiculos_disponibles = models.Vehiculo.objects.filter(estado='DISPONIBLE').count()

    data = {
        'total_clientes': total_clientes,
        'total_vehiculos': total_vehiculos,
        'total_reservas': total_reservas,
        'vehiculos_disponibles': vehiculos_disponibles,
        'ultimos_clientes': models.Cliente.objects.all().order_by('-fecha_creacion')[:5],
        'ultimos_vehiculos': models.Vehiculo.objects.all().order_by('-fecha_ingreso')[:5],
    }
    return render(request, 'clientes_inventario_home.html', data)


def imagen_vehiculo(vehiculo):
    imagenes = {
        'TOYOTA': 'https://tuyomotor.com/wp-content/uploads/2025/08/TUYO_COROLLA-26-2-scaled.jpg',
        'CHEVROLET': 'https://octane.rent/wp-content/uploads/2023/06/chevrolet-camaro-blue-41-600x400.webp',
        'BMW': 'https://noticias.pro.pvt.coches.com/wp-content/uploads/2018/06/BMW-X5-2019-12.jpg?force_format=original&w=1280&h=720',
        'MERCEDES': 'https://objetos.estaticos-marca.com/assets/multimedia/imagenes/2019/02/20/15506779401989.jpg',
        'AUDI': 'https://i.pinimg.com/736x/24/6b/78/246b78f4ad72bef384f7d509b3128124.jpg',
    }
    return imagenes.get(
        vehiculo.marca.upper(),
        'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=900&auto=format&fit=crop'
    )


def inventario(request):
    vehiculos = models.Vehiculo.objects.all().order_by('marca', 'modelo')

    for vehiculo in vehiculos:
        vehiculo.tiene_reserva = vehiculo.reservas.filter(activa=True).exists()
        vehiculo.imagen = imagen_vehiculo(vehiculo)

    return render(request, 'inventario.html', {'vehiculos': vehiculos})


def crear_vehiculo(request):
    if request.method == 'POST':
        models.Vehiculo.objects.create(
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            anio=request.POST['anio'],
            placa=request.POST['placa'].upper(),
            color=request.POST['color'],
            precio=request.POST['precio'],
            estado=request.POST['estado'],
        )
        messages.success(request, 'Vehiculo creado correctamente.')
        return redirect('inventario')

    return render(request, 'formulario_vehiculo.html', {'estados': models.Vehiculo.ESTADOS})


def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(models.Vehiculo, id=vehiculo_id)

    if request.method == 'POST':
        vehiculo.marca = request.POST['marca']
        vehiculo.modelo = request.POST['modelo']
        vehiculo.anio = request.POST['anio']
        vehiculo.placa = request.POST['placa'].upper()
        vehiculo.color = request.POST['color']
        vehiculo.precio = request.POST['precio']
        vehiculo.estado = request.POST['estado']
        vehiculo.save()
        messages.success(request, 'Vehiculo actualizado correctamente.')
        return redirect('inventario')

    data = {'vehiculo': vehiculo, 'estados': models.Vehiculo.ESTADOS}
    return render(request, 'formulario_vehiculo.html', data)


def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(models.Vehiculo, id=vehiculo_id)

    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehiculo eliminado correctamente.')
        return redirect('inventario')

    return render(request, 'confirmar_eliminar.html', {'objeto': vehiculo, 'volver': 'inventario'})


def clientes(request):
    lista_clientes = models.Cliente.objects.all().order_by('nombre')
    return render(request, 'clientes.html', {'lista_clientes': lista_clientes})


def crear_cliente(request):
    if request.method == 'POST':
        models.Cliente.objects.create(
            nombre=request.POST['nombre'],
            documento=request.POST['documento'],
            email=request.POST['email'],
            telefono=request.POST.get('telefono', ''),
            direccion=request.POST.get('direccion', ''),
            activo=request.POST.get('activo') == 'on',
        )
        messages.success(request, 'Cliente creado correctamente.')
        return redirect('clientes')

    return render(request, 'formulario_cliente.html')


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(models.Cliente, id=cliente_id)

    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.documento = request.POST['documento']
        cliente.email = request.POST['email']
        cliente.telefono = request.POST.get('telefono', '')
        cliente.direccion = request.POST.get('direccion', '')
        cliente.activo = request.POST.get('activo') == 'on'
        cliente.save()
        messages.success(request, 'Cliente actualizado correctamente.')
        return redirect('clientes')

    return render(request, 'formulario_cliente.html', {'cliente': cliente})


def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(models.Cliente, id=cliente_id)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('clientes')

    return render(request, 'confirmar_eliminar.html', {'objeto': cliente, 'volver': 'clientes'})


def reservas(request):
    lista_reservas = models.Reserva.objects.select_related('cliente', 'vehiculo').all().order_by('-fecha_reserva')
    return render(request, 'reservas.html', {'lista_reservas': lista_reservas})


def crear_reserva(request):
    if request.method == 'POST':
        cliente = get_object_or_404(models.Cliente, id=request.POST['cliente'])
        vehiculo = get_object_or_404(models.Vehiculo, id=request.POST['vehiculo'])
        models.Reserva.objects.create(cliente=cliente, vehiculo=vehiculo)
        vehiculo.estado = 'RESERVADO'
        vehiculo.save()
        messages.success(request, 'Reserva creada correctamente.')
        return redirect('reservas')

    data = {
        'clientes': models.Cliente.objects.filter(activo=True).order_by('nombre'),
        'vehiculos': models.Vehiculo.objects.exclude(estado='VENDIDO').order_by('marca', 'modelo'),
    }
    return render(request, 'formulario_reserva.html', data)


def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(models.Reserva, id=reserva_id)

    if request.method == 'POST':
        reserva.activa = False
        reserva.save()
        if not reserva.vehiculo.reservas.filter(activa=True).exclude(id=reserva.id).exists():
            reserva.vehiculo.estado = 'DISPONIBLE'
            reserva.vehiculo.save()
        messages.success(request, 'Reserva cancelada correctamente.')

    return redirect('reservas')
