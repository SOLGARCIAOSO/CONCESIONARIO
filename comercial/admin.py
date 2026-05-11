from django.contrib import admin
from .models import Cotizaciones, Reservas, Ventas

# Register your models here.

from .models import Cotizaciones
from .models import Reservas
from .models import Ventas

admin.site.register(Cotizaciones)
admin.site.register(Reservas)
admin.site.register(Ventas)