from django.contrib import messages
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .models import Factura, Pago, PlanCuotas


# ── HELPERS ──────────────────────────────────────────────────────────────────

def _calcular_saldo(factura):
    total_pagado = factura.pagos.aggregate(total=Sum('monto'))['total'] or 0
    saldo = float(factura.total) - float(total_pagado)
    return float(total_pagado), max(saldo, 0)


# ── HOME / DASHBOARD ─────────────────────────────────────────────────────────

def home(request):
    total_pagado_global = Pago.objects.aggregate(total=Sum('monto'))['total'] or 0

    data = {
        'total_facturas':      Factura.objects.count(),
        'facturas_pagadas':    Factura.objects.filter(estado='pagada').count(),
        'facturas_pendientes': Factura.objects.filter(estado='pendiente').count(),
        'total_recaudado':     total_pagado_global,
        'ultimas_facturas':    Factura.objects.order_by('-fecha_emision')[:5],
        'ultimos_pagos':       Pago.objects.select_related('factura').order_by('-fecha')[:5],
    }
    return render(request, 'pagos/home.html', data)


# ── FACTURAS ──────────────────────────────────────────────────────────────────

def lista_facturas(request):
    qs = Factura.objects.all().order_by('-fecha_emision')

    q      = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    if q:
        qs = qs.filter(
            Q(numero_factura__icontains=q) |
            Q(cliente__icontains=q) |
            Q(vehiculo__icontains=q)
        )
    if estado:
        qs = qs.filter(estado=estado)

    return render(request, 'pagos/facturas.html', {'lista_facturas': qs})


def detalle_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    pagos   = factura.pagos.all().order_by('fecha')

    total_pagado, saldo_pendiente = _calcular_saldo(factura)
    porcentaje = (total_pagado / float(factura.total) * 100) if factura.total else 0

    # Plan de cuotas si existe
    plan = getattr(factura, 'plan_cuotas', None)

    data = {
        'factura':           factura,
        'pagos':             pagos,
        'total_pagado':      total_pagado,
        'saldo_pendiente':   saldo_pendiente,
        'porcentaje_pagado': min(porcentaje, 100),
        'plan':              plan,
    }
    return render(request, 'pagos/detalle_factura.html', data)


def crear_factura(request):
    if request.method == 'POST':
        try:
            Factura.objects.create(
                numero_factura=request.POST['numero_factura'].strip().upper(),
                cliente=request.POST['cliente'].strip(),
                vehiculo=request.POST['vehiculo'].strip(),
                total=request.POST['total'],
                estado=request.POST['estado'],
            )
            messages.success(request, 'Factura creada correctamente.')
            return redirect('lista-facturas')
        except Exception as e:
            messages.error(request, f'Error al crear la factura: {e}')

    return render(request, 'pagos/formulario_factura.html')


def editar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    if request.method == 'POST':
        try:
            factura.numero_factura = request.POST['numero_factura'].strip().upper()
            factura.cliente        = request.POST['cliente'].strip()
            factura.vehiculo       = request.POST['vehiculo'].strip()
            factura.total          = request.POST['total']
            factura.estado         = request.POST['estado']
            factura.save()
            messages.success(request, 'Factura actualizada correctamente.')
            return redirect('lista-facturas')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')

    return render(request, 'pagos/formulario_factura.html', {'factura': factura})


def eliminar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    if request.method == 'POST':
        factura.delete()
        messages.success(request, 'Factura eliminada correctamente.')
        return redirect('lista-facturas')

    return render(request, 'pagos/confirmar_eliminar.html', {
        'objeto':     factura,
        'volver_url': '/pagos/facturas/',
    })


def marcar_factura_pagada(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    factura.estado = 'pagada'
    factura.save()
    messages.success(request, f'Factura {factura.numero_factura} marcada como pagada.')
    return redirect('detalle-factura', factura_id=factura_id)


# ── PAGOS ─────────────────────────────────────────────────────────────────────

def lista_pagos(request):
    qs = Pago.objects.select_related('factura').all().order_by('-fecha')

    tipo = request.GET.get('tipo', '').strip()
    if tipo:
        qs = qs.filter(tipo_pago=tipo)

    return render(request, 'pagos/pagos_lista.html', {'lista_pagos': qs})


def crear_pago(request):
    factura_preseleccionada = None
    saldo_pendiente = None
    plan_existente = None

    factura_id = request.GET.get('factura') or request.POST.get('factura')
    if factura_id:
        factura_preseleccionada = Factura.objects.filter(id=factura_id).first()
        if factura_preseleccionada:
            _, saldo_pendiente = _calcular_saldo(factura_preseleccionada)
            plan_existente = getattr(factura_preseleccionada, 'plan_cuotas', None)

    if request.method == 'POST':
        tipo_pago = request.POST.get('tipo_pago')
        modo_cuota = request.POST.get('modo_cuota', 'manual')  # 'plan' o 'manual'

        try:
            factura = get_object_or_404(Factura, id=request.POST['factura'])
            _, saldo = _calcular_saldo(factura)

            if tipo_pago == 'financiacion' and modo_cuota == 'plan':
                # ── Crear plan de cuotas automático ──────────────────────────
                num_cuotas = int(request.POST.get('numero_cuotas', 1))
                if num_cuotas < 1:
                    raise ValueError('El número de cuotas debe ser al menos 1.')

                valor_cuota = round(saldo / num_cuotas, 2)

                # Guardar o actualizar el plan
                PlanCuotas.objects.update_or_create(
                    factura=factura,
                    defaults={
                        'numero_cuotas': num_cuotas,
                        'valor_cuota':   valor_cuota,
                    }
                )

                # Registrar la primera cuota inmediatamente
                Pago.objects.create(
                    factura=factura,
                    monto=valor_cuota,
                    tipo_pago='financiacion',
                )
                messages.success(
                    request,
                    f'Plan creado: {num_cuotas} cuotas de $ {valor_cuota:,.0f}. '
                    f'Primera cuota registrada.'
                )

            else:
                # ── Pago manual (contado o cuota manual) ─────────────────────
                monto = request.POST.get('monto')
                if not monto:
                    raise ValueError('Ingresa un monto.')

                Pago.objects.create(
                    factura=factura,
                    monto=monto,
                    tipo_pago=tipo_pago,
                )
                messages.success(request, 'Pago registrado correctamente.')

            # Marcar pagada si saldo llega a 0
            _, saldo_nuevo = _calcular_saldo(factura)
            if saldo_nuevo <= 0 and factura.estado != 'pagada':
                factura.estado = 'pagada'
                factura.save()

            return redirect('detalle-factura', factura_id=factura.id)

        except Exception as e:
            messages.error(request, f'Error: {e}')

    data = {
        'facturas':                Factura.objects.filter(estado='pendiente').order_by('-fecha_emision'),
        'factura_preseleccionada': factura_preseleccionada,
        'saldo_pendiente':         saldo_pendiente,
        'plan_existente':          plan_existente,
    }
    return render(request, 'pagos/formulario_pago.html', data)


def editar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)

    if request.method == 'POST':
        try:
            pago.factura   = get_object_or_404(Factura, id=request.POST['factura'])
            pago.monto     = request.POST['monto']
            pago.tipo_pago = request.POST['tipo_pago']
            pago.save()
            messages.success(request, 'Pago actualizado correctamente.')
            return redirect('lista-pagos')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {e}')

    data = {
        'pago':     pago,
        'facturas': Factura.objects.all().order_by('-fecha_emision'),
    }
    return render(request, 'pagos/formulario_pago.html', data)


def eliminar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)

    if request.method == 'POST':
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente.')
        return redirect('lista-pagos')

    return render(request, 'pagos/confirmar_eliminar.html', {
        'objeto':     f'Pago de $ {pago.monto} — {pago.factura.numero_factura}',
        'volver_url': '/pagos/pagos/',
    })


# ── CUOTAS ────────────────────────────────────────────────────────────────────

def cuotas(request):
    facturas_con_financiacion = Factura.objects.filter(
        pagos__tipo_pago='financiacion'
    ).distinct().order_by('-fecha_emision')

    items = []
    for factura in facturas_con_financiacion:
        pagos_factura = factura.pagos.filter(tipo_pago='financiacion').order_by('fecha')
        total_pagado, saldo = _calcular_saldo(factura)
        porcentaje = (total_pagado / float(factura.total) * 100) if factura.total else 0
        plan = getattr(factura, 'plan_cuotas', None)

        cuotas_pagadas = pagos_factura.count()
        cuotas_totales = plan.numero_cuotas if plan else None

        items.append({
            'factura':        factura,
            'pagos':          pagos_factura,
            'total_pagado':   total_pagado,
            'saldo_pendiente': saldo,
            'porcentaje':     min(porcentaje, 100),
            'plan':           plan,
            'cuotas_pagadas': cuotas_pagadas,
            'cuotas_totales': cuotas_totales,
        })

    return render(request, 'pagos/cuotas.html', {'facturas_financiacion': items})