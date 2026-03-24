from django.contrib import admin
from .models import Cliente, Vehiculo, Reserva

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Reserva)
