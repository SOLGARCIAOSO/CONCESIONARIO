import uuid
from django.db import models

class TipoDocumento(models.TextChoices):
    CC = "CC", "Cédula de Ciudadanía"
    CE = "CE", "Cédula de Extranjería"
    NIT = "NIT", "NIT"
    PAS = "PAS", "Pasaporte"

class RolEnum(models.TextChoices):
    ADMINISTRADOR = "ADMIN", "Administrador"
    GERENTE = "GER", "Gerente"
    VENDEDOR = "VEN", "Vendedor"
    RECEPCIONISTA = "REC", "Recepcionista"
    MECANICO = "MEC", "Mecánico"
    CONTADOR = "CON", "Contador"
    CLIENTE = "CLI", "Cliente"

class Tercero(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=TipoDocumento.choices)
    numero_documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=150, blank=True)
    email = models.EmailField()

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - {self.numero_documento}"

class Permiso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=60, choices=RolEnum.choices, unique=True)
    permisos = models.ManyToManyField(
        Permiso,
        related_name="roles",
        blank=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    tercero = models.OneToOneField(
        Tercero,
        on_delete=models.CASCADE,
        related_name="usuario"
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name="usuarios"
    )

    contrasena = models.CharField(max_length=128)
    habilitado = models.BooleanField(default=True)
    cuenta_activa = models.BooleanField(default=False)

    uuid_publico = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Usuario: {self.tercero.nombre} - Rol: {self.rol.nombre}"