from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('home/',                                   views.home,                  name='home-pagos'),

    # Facturas
    path('facturas/',                               views.lista_facturas,         name='lista-facturas'),
    path('facturas/crear/',                         views.crear_factura,          name='crear-factura'),
    path('facturas/<int:factura_id>/',              views.detalle_factura,        name='detalle-factura'),
    path('facturas/editar/<int:factura_id>/',       views.editar_factura,         name='editar-factura'),
    path('facturas/eliminar/<int:factura_id>/',     views.eliminar_factura,       name='eliminar-factura'),
    path('facturas/<int:factura_id>/marcar-pagada/', views.marcar_factura_pagada, name='marcar-pagada'),

    # Pagos
    path('pagos/',                                  views.lista_pagos,            name='lista-pagos'),
    path('pagos/crear/',                            views.crear_pago,             name='crear-pago'),
    path('pagos/editar/<int:pago_id>/',             views.editar_pago,            name='editar-pago'),
    path('pagos/eliminar/<int:pago_id>/',           views.eliminar_pago,          name='eliminar-pago'),

    # Cuotas
    path('cuotas/',                                 views.cuotas,                 name='cuotas'),
]