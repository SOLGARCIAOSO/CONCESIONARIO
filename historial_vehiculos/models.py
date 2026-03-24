from django.db import models



class InformacionTecnica(models.Model):

    vehiculo = models.OneToOneField(
        'clientes_inventario.Vehiculo',
        on_delete=models.CASCADE,
        related_name='info_tecnica'
    )

    motor = models.CharField(max_length=100)
    transmision = models.CharField(max_length=50)
    tipo_combustible = models.CharField(max_length=50)
    cilindraje = models.PositiveIntegerField(help_text="centimetros cubicos")
    numero_chasis = models.CharField(max_length=100, unique=True)
    numero_motor = models.CharField(max_length=100, unique=True)
    capacidad_pasajeros = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ficha tecnica - {self.vehiculo.placa}"


class Mantenimiento(models.Model):

    vehiculo = models.ForeignKey(
        'clientes_inventario.Vehiculo',
        on_delete=models.CASCADE,
        related_name='mantenimientos'
    )

    fecha = models.DateField()
    descripcion = models.TextField()
    kilometraje = models.PositiveIntegerField()
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taller = models.CharField(max_length=100)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"mantenimiento {self.fecha} - {self.vehiculo.placa}"


class PropietarioAnterior(models.Model):

    vehiculo = models.ForeignKey(
        'clientes_inventario.Vehiculo',
        on_delete=models.CASCADE,
        related_name='propietarios'
    )

    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.vehiculo.placa}"
