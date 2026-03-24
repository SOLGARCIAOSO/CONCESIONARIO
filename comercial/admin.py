from django.contrib import admin

# Register your models here.

from .models import Cotizacion 
from .models import Reserva
from .models import Venta 

admin.site.register(Cotizacion)
admin.site.register(Reserva)
admin.site.register(Venta)