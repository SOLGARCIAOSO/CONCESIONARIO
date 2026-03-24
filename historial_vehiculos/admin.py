from django.contrib import admin
from .models import InformacionTecnica, Mantenimiento, PropietarioAnterior

# Register your models here.

admin.site.register(InformacionTecnica)
admin.site.register(Mantenimiento)
admin.site.register(PropietarioAnterior)
