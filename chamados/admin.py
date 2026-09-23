from django.contrib import admin
from .models import Chamado


@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'solicitante',
        'setor',
        'tipo',
        'prioridade',
        'status',
        'responsavel',
        'data_abertura',
    )

    list_filter = (
        'status',
        'prioridade',
        'tipo',
        'setor',
    )

    search_fields = (
        'solicitante__username',
        'solicitante__first_name',
        'solicitante__last_name',
        'descricao',
    )