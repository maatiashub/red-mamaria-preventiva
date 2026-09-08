from django.contrib import admin
from .models import PreguntaEducativa, AnalisisEcografia

@admin.register(PreguntaEducativa)
class PreguntaEducativaAdmin(admin.ModelAdmin):
    # Columnas que se verán en la lista
    list_display = ('sesion', 'enunciado_corto', 'respuesta_correcta', 'fecha_creacion')
    # Filtros laterales
    list_filter = ('sesion', 'respuesta_correcta')
    # Buscador por texto
    search_fields = ('enunciado', 'explicacion_medica')

    def enunciado_corto(self, obj):
        return obj.enunciado[:60] + "..." if len(obj.enunciado) > 60 else obj.enunciado
    enunciado_corto.short_description = "Pregunta / Mito"


@admin.register(AnalisisEcografia)
class AnalisisEcografiaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'porcentaje_riesgo', 'rango_alerta', 'fecha_analisis')
    list_filter = ('rango_alerta', 'fecha_analisis')
    search_fields = ('usuario__username', 'rango_alerta')
    readonly_fields = ('fecha_analisis',)