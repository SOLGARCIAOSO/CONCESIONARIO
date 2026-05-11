
from django.db import models


 
class Cotizaciones(models.Model):
  id_cotizacion = models.AutoField(primary_key=True)
  vehiculo_id = models.IntegerField()
  cliente_id = models.IntegerField()
  num_cotizacion = models.CharField(max_length=50, unique=True)
  fecha_creacion = models.DateField(auto_now_add=True)
  fecha_vencimiento = models.DateField()
  precio_base = models.DecimalField(max_digits=12, decimal_places=2)
  total = models.DecimalField(max_digits=12, decimal_places=2)
  estado = models.CharField(max_length=20, default="Pendiente")
    
  def __str__(self):
    return f"Cotización: {self.num_cotizacion} {self.cliente_id}"
  

class Reservas(models.Model):
  id_reserva = models.AutoField(primary_key=True)
  vehiculo_id = models.IntegerField()
  cliente_id = models.IntegerField()
  fecha_reserva = models.DateTimeField(auto_now_add=True)
  monto_apartado = models.DecimalField(max_digits=10, decimal_places=2)
  activa = models.BooleanField(default=True)
  notas = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"Reserva {self.vehiculo_id} -  {self.cliente_id}"
  

class Ventas(models.Model):
  id_venta = models.IntegerField(primary_key=True)
  vehiculo_id = models.IntegerField()
  cliente_id = models.IntegerField()
  vendedor_id = models.IntegerField()
  fecha = models.DateField(auto_now_add=True)
  precio = models.DecimalField(max_digits=12, decimal_places=2)
  total = models.DecimalField(max_digits=12, decimal_places=2)
  estado = models.CharField(max_length=20, default='Completada')
  num_factura = models.CharField(max_length=50, unique=True)
  tipo_de_pago = models.CharField(max_length=20,)
    
def __str__(self):
   return f"Venta: {self.id_venta} - {self.estado}"
  
  
  

