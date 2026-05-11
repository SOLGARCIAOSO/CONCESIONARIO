from django import forms

class CotizacionForm(forms.Form):
  
  id_cotizacion = forms.IntegerField(label='ID Cotizacion')
  vehiculo_id = forms.IntegerField(label='ID Vehiculo')
  cliente_id = forms.IntegerField(label='ID Cliente')
  num_cotizacion = forms.CharField(label='Numero Cotizacion', max_length=50)
  fecha_creacion = forms.DateField(label='Fecha Creacion',widget=forms.DateInput(attrs={'type': 'date'}))
  fecha_vencimiento = forms.DateField( label='Fecha Vencimiento', widget=forms.DateInput(attrs={'type': 'date'}))
  precio_base = forms.DecimalField( label='Precio Base',max_digits=12, decimal_places=2)
  total = forms.DecimalField(label='Total', max_digits=12, decimal_places=2)
  estado = forms.CharField( label='Estado',max_length=30)

class ReservaForm(forms.Form):

  id_reserva = forms.IntegerField(label='ID Reserva')
  vehiculo_id = forms.IntegerField(label='ID Vehiculo')
  cliente_id = forms.IntegerField(label='ID Cliente')
  fecha_reserva = forms.DateField(label='Fecha Reserva', widget=forms.DateInput(attrs={'type': 'date'}))
  monto_apartado = forms.DecimalField(label='Monto Apartado', max_digits=12, decimal_places=2)
  activa = forms.BooleanField(label='Reserva Activa', required=False)
  notas = forms.CharField(label='Notas',required=False,widget=forms.Textarea)

class VentaForm(forms.Form):

    id_venta = forms.IntegerField(label='ID Venta')
    vehiculo_id = forms.IntegerField(label='ID Vehículo')
    cliente_id = forms.IntegerField(label='ID Cliente')
    vendedor_id = forms.IntegerField(label='ID Vendedor')
    fecha = forms.DateField(label='Fecha Venta', widget=forms.DateInput(attrs={'type': 'date'}))
    precio = forms.DecimalField(label='Precio', max_digits=12, decimal_places=2)
    total = forms.DecimalField(label='Total', max_digits=12, decimal_places=2)
    estado = forms.CharField(label='Estado', max_length=30)
    num_factura = forms.CharField(label='Número Factura', max_length=50)
    tipo_de_pago = forms.CharField(label='Tipo de Pago',max_length=50)