from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from .forms import CotizacionForm, ReservaForm, VentaForm


def home(request):

    data_envio = {
        'total_cot': models.Cotizaciones.objects.count(),
        'total_res': models.Reservas.objects.filter(activa=True).count(),
        'total_ven': models.Ventas.objects.count(),
        'cotizaciones': models.Cotizaciones.objects.order_by('fecha_creacion')[:5],
        'reservas': models.Reservas.objects.order_by('fecha_reserva')[:5],
        'ventas': models.Ventas.objects.order_by('fecha')[:5],
    }

    return render(request, 'index.html', data_envio)


def lista_cotizaciones(request):

    data = models.Cotizaciones.objects.all()

    data_envio = {
        'cotizaciones': data
    }

    return render(request, 'lista_cotizaciones.html', data_envio)


def lista_reservas(request):

    data = models.Reservas.objects.all()

    data_envio = {
        'reservas': data
    }

    return render(request, 'lista_reservas.html', data_envio)


def lista_ventas(request):

    data = models.Ventas.objects.all()

    data_envio = {
        'ventas': data
    }
    return render(request, 'lista_ventas.html', data_envio)


def crear_cotizacion(request):

    if request.method == 'POST':

        form = CotizacionForm(request.POST)

        if form.is_valid():
            
             models.Cotizaciones.objects.create(

                id_cotizacion=form.cleaned_data['id_cotizacion'],
                vehiculo_id=form.cleaned_data['vehiculo_id'],
                cliente_id=form.cleaned_data['cliente_id'],
                num_cotizacion=form.cleaned_data['num_cotizacion'],
                fecha_creacion=form.cleaned_data['fecha_creacion'],
                fecha_vencimiento=form.cleaned_data['fecha_vencimiento'],
                precio_base=form.cleaned_data['precio_base'],
                total=form.cleaned_data['total'],
                estado=form.cleaned_data['estado']

            )

             return redirect('/comercial/lista_cotizaciones/')

    else:

        form = CotizacionForm()

    return render(request, 'crear_cotizacion.html', {
        'form': form
    })


def crear_reserva(request):

    if request.method == 'POST':

        form = ReservaForm(request.POST)

        if form.is_valid():

            models.Reservas.objects.create(

                id_reserva=form.cleaned_data['id_reserva'],
                vehiculo_id=form.cleaned_data['vehiculo_id'],
                cliente_id=form.cleaned_data['cliente_id'],
                fecha_reserva=form.cleaned_data['fecha_reserva'],
                monto_apartado=form.cleaned_data['monto_apartado'],
                activa=form.cleaned_data['activa'],
                notas=form.cleaned_data['notas']

            )

            return redirect('/comercial/lista_reservas/')

    else:

        form = ReservaForm()

    return render(request, 'crear_reserva.html', {
        'form': form
    })


def crear_venta(request):

    if request.method == 'POST':

        form = VentaForm(request.POST)

        if form.is_valid():

             models.Ventas.objects.create(

                id_venta=form.cleaned_data['id_venta'],
                vehiculo_id=form.cleaned_data['vehiculo_id'],
                cliente_id=form.cleaned_data['cliente_id'],
                vendedor_id=form.cleaned_data['vendedor_id'],
                fecha=form.cleaned_data['fecha'],
                precio=form.cleaned_data['precio'],
                total=form.cleaned_data['total'],
                estado=form.cleaned_data['estado'],
                num_factura=form.cleaned_data['num_factura'],
                tipo_de_pago=form.cleaned_data['tipo_de_pago']

             )

             return redirect('/comercial/')

    else:

        form = VentaForm()

    return render(request, 'crear_venta.html', {
        'form': form
    })