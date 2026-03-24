from django.db import models


class Factura(models.Model):

    ESTADO_FACTURA = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
    ]

    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.CharField(max_length=100)
    vehiculo = models.CharField(max_length=100)
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_FACTURA,
        default='pendiente'
    )

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente}"


class Pago(models.Model):

    TIPO_PAGO = [
        ('contado', 'Contado'),
        ('financiacion', 'Financiación'),
    ]

    factura = models.ForeignKey(
        Factura,
        on_delete=models.CASCADE,
        related_name="pagos"
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    tipo_pago = models.CharField(max_length=20, choices=TIPO_PAGO)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id} - {self.factura.numero_factura}"