from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from . import models


# ── HELPERS ──────────────────────────────────────────────────────────────────

IMAGENES_VEHICULO = {
    'TOYOTA':    'https://tuyomotor.com/wp-content/uploads/2025/08/TUYO_COROLLA-26-2-scaled.jpg',
    'CHEVROLET': 'https://octane.rent/wp-content/uploads/2023/06/chevrolet-camaro-blue-41-600x400.webp',
    'BMW':       'https://noticias.pro.pvt.coches.com/wp-content/uploads/2018/06/BMW-X5-2019-12.jpg?force_format=original&w=1280&h=720',
    'MERCEDES':  'https://objetos.estaticos-marca.com/assets/multimedia/imagenes/2019/02/20/15506779401989.jpg',
    'AUDI':      'https://i.pinimg.com/736x/24/6b/78/246b78f4ad72bef384f7d509b3128124.jpg',
    'MAZDA':     'https://images.unsplash.com/photo-1616422285623-13ff0162193c?w=600&auto=format&fit=crop',
    'FORD':      'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=600&auto=format&fit=crop',
    'HONDA':     'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=600&auto=format&fit=crop',
    'NISSAN':    'https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=600&auto=format&fit=crop',
}
IMAGEN_DEFAULT = 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=600&auto=format&fit=crop'


def _imagen_vehiculo(vehiculo):
    return IMAGENES_VEHICULO.get(vehiculo.marca.upper(), IMAGEN_DEFAULT)


# ── HOME / DASHBOARD ──────────────────────────────────────────────────────────

def home(request):
    data = {
        'total_clientes':       models.Cliente.objects.count(),
        'total_vehiculos':      models.Vehiculo.objects.count(),
        'total_reservas':       models.Reserva.objects.filter(activa=True).count(),
        'vehiculos_disponibles': models.Vehiculo.objects.filter(estado='DISPONIBLE').count(),
        'ultimos_clientes':     models.Cliente.objects.order_by('-fecha_creacion')[:5],
        'ultimos_vehiculos':    models.Vehiculo.objects.order_by('-fecha_ingreso')[:5],
    }
    return render(request, 'clientes_inventario/clientes_inventario_home.html', data)


# ── INVENTARIO ────────────────────────────────────────────────────────────────

def inventario(request):
    qs = models.Vehiculo.objects.all().order_by('marca', 'modelo')

    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    if q:
        qs = qs.filter(
            Q(marca__icontains=q) |
            Q(modelo__icontains=q) |
            Q(placa__icontains=q)
        )
    if estado:
        qs = qs.filter(estado=estado)

    for v in qs:
        v.tiene_reserva = v.reservas.filter(activa=True).exists()
        v.imagen = _imagen_vehiculo(v)

    return render(request, 'clientes_inventario/inventario.html', {'vehiculos': qs})


def crear_vehiculo(request):
    if request.method == 'POST':
        try:
            models.Vehiculo.objects.create(
                marca=request.POST['marca'].strip().title(),
                modelo=request.POST['modelo'].strip(),
                anio=request.POST['anio'],
                placa=request.POST['placa'].strip().upper(),
                color=request.POST['color'].strip(),
                precio=request.POST['precio'],
                estado=request.POST['estado'],
            )
            messages.success(request, 'Vehículo creado correctamente.')
            return redirect('inventario')
        except Exception as e:
            messages.error(request, f'Error al crear el vehículo: {e}')

    return render(request, 'clientes_inventario/formulario_vehiculo.html', {'estados': models.Vehiculo.ESTADOS})


def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(models.Vehiculo, id=vehiculo_id)

    if request.method == 'POST':
        try:
            vehiculo.marca  = request.POST['marca'].strip().title()
            vehiculo.modelo = request.POST['modelo'].strip()
            vehiculo.anio   = request.POST['anio']
            vehiculo.placa  = request.POST['placa'].strip().upper()
            vehiculo.color  = request.POST['color'].strip()
            vehiculo.precio = request.POST['precio']
            vehiculo.estado = request.POST['estado']
            vehiculo.save()
            messages.success(request, 'Vehículo actualizado correctamente.')
            return redirect('inventario')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')

    data = {'vehiculo': vehiculo, 'estados': models.Vehiculo.ESTADOS}
    return render(request, 'clientes_inventario/formulario_vehiculo.html', data)


def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(models.Vehiculo, id=vehiculo_id)

    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado correctamente.')
        return redirect('inventario')

    return render(request, 'clientes_inventario/confirmar_eliminar.html', {'objeto': vehiculo, 'volver': 'inventario'})


# ── CLIENTES ──────────────────────────────────────────────────────────────────

def clientes(request):
    qs = models.Cliente.objects.all().order_by('nombre')

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) |
            Q(documento__icontains=q)
        )

    return render(request, 'clientes_inventario/clientes.html', {'lista_clientes': qs})


def crear_cliente(request):
    if request.method == 'POST':
        try:
            models.Cliente.objects.create(
                nombre=request.POST['nombre'].strip(),
                documento=request.POST['documento'].strip(),
                email=request.POST['email'].strip(),
                telefono=request.POST.get('telefono', '').strip(),
                direccion=request.POST.get('direccion', '').strip(),
                activo=request.POST.get('activo') == 'on',
            )
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('clientes')
        except Exception as e:
            messages.error(request, f'Error al crear el cliente: {e}')

    return render(request, 'clientes_inventario/formulario_cliente.html')


def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(models.Cliente, id=cliente_id)

    if request.method == 'POST':
        try:
            cliente.nombre    = request.POST['nombre'].strip()
            cliente.documento = request.POST['documento'].strip()
            cliente.email     = request.POST['email'].strip()
            cliente.telefono  = request.POST.get('telefono', '').strip()
            cliente.direccion = request.POST.get('direccion', '').strip()
            cliente.activo    = request.POST.get('activo') == 'on'
            cliente.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('clientes')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')

    return render(request, 'clientes_inventario/formulario_cliente.html', {'cliente': cliente})


def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(models.Cliente, id=cliente_id)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('clientes')

    return render(request, 'clientes_inventario/confirmar_eliminar.html', {'objeto': cliente, 'volver': 'clientes'})


# ── RESERVAS ──────────────────────────────────────────────────────────────────

def reservas(request):
    lista_reservas = (
        models.Reserva.objects
        .select_related('cliente', 'vehiculo')
        .all()
        .order_by('-fecha_reserva')
    )
    return render(request, 'clientes_inventario/reservas.html', {'lista_reservas': lista_reservas})


def crear_reserva(request):
    if request.method == 'POST':
        try:
            cliente  = get_object_or_404(models.Cliente, id=request.POST['cliente'])
            vehiculo = get_object_or_404(models.Vehiculo, id=request.POST['vehiculo'])

            models.Reserva.objects.create(cliente=cliente, vehiculo=vehiculo)
            vehiculo.estado = 'RESERVADO'
            vehiculo.save()

            messages.success(request, f'Reserva creada para {cliente.nombre}.')
            return redirect('reservas')
        except Exception as e:
            messages.error(request, f'Error al crear la reserva: {e}')

    data = {
        'clientes':  models.Cliente.objects.filter(activo=True).order_by('nombre'),
        'vehiculos': models.Vehiculo.objects.exclude(estado='VENDIDO').order_by('marca', 'modelo'),
    }
    return render(request, 'clientes_inventario/formulario_reserva.html', data)


def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(models.Reserva, id=reserva_id)

    if request.method == 'POST':
        reserva.activa = False
        reserva.save()

        # Si no quedan reservas activas, el vehículo vuelve a disponible
        if not reserva.vehiculo.reservas.filter(activa=True).exists():
            reserva.vehiculo.estado = 'DISPONIBLE'
            reserva.vehiculo.save()

        messages.success(request, 'Reserva cancelada correctamente.')

    return redirect('reservas')
