from django.contrib import admin
from .models import Equipo, Jugador, Partido


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_fifa', 'grupo', 'confederacion')
    list_filter = ('grupo', 'confederacion')
    search_fields = ('nombre', 'codigo_fifa')
    ordering = ('grupo', 'nombre')


@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equipo', 'posicion', 'numero_camiseta', 'edad')
    list_filter = ('equipo__grupo', 'posicion')
    search_fields = ('nombre', 'equipo__nombre')
    autocomplete_fields = ('equipo',)


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = (
        'grupo', 'jornada', 'equipo_local', 'equipo_visitante',
        'fecha_hora', 'goles_local', 'goles_visitante', 'estado'
    )
    list_filter = ('grupo', 'jornada', 'estado')
    list_editable = ('goles_local', 'goles_visitante', 'estado')
    search_fields = ('equipo_local__nombre', 'equipo_visitante__nombre')
    ordering = ('grupo', 'jornada', 'fecha_hora')
    date_hierarchy = 'fecha_hora'

    fieldsets = (
        ('Datos del partido', {
            'fields': (
                ('equipo_local', 'equipo_visitante'),
                ('grupo', 'jornada'),
                ('fecha_hora', 'estadio', 'ciudad'),
            )
        }),
        ('Resultado', {
            'fields': (
                ('goles_local', 'goles_visitante'),
                'estado',
            )
        }),
    )
