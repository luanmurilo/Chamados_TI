from .models import Chamado
from django.contrib import admin, messages
from .models import ConfiguracaoEmail
from .services.email_service import enviar_email


@admin.register(ConfiguracaoEmail)
class ConfiguracaoEmailAdmin(admin.ModelAdmin):

    list_display = (
        'nome',
        'servidor_smtp',
        'porta_smtp',
        'email_remetente',
        'email_ti',
        'ativo',
        'data_atualizacao',
    )

    list_filter = (
        'ativo',
        'usar_tls',
        'usar_ssl',
    )

    search_fields = (
        'nome',
        'servidor_smtp',
        'email_remetente',
        'email_ti',
    )

    actions = [
        'enviar_email_teste',
    ]

    @admin.action(description='Enviar e-mail de teste')
    def enviar_email_teste(self, request, queryset):

        for configuracao in queryset:

            try:

                enviar_email(
                    destinatarios=configuracao.email_ti,
                    assunto='Teste de e-mail - Sistema de Chamados TI',
                    mensagem=(
                        'Este é um e-mail de teste do Sistema de Chamados TI.\n\n'
                        'A configuração de e-mail foi carregada corretamente '
                        'e o sistema conseguiu realizar o envio.'
                    ),
                )

                self.message_user(
                    request,
                    (
                        f'E-mail de teste enviado com sucesso para '
                        f'{configuracao.email_ti}.'
                    ),
                    messages.SUCCESS,
                )

            except Exception as erro:

                self.message_user(
                    request,
                    (
                        f'Erro ao enviar e-mail usando a configuração '
                        f'"{configuracao.nome}": {erro}'
                    ),
                    messages.ERROR,
                )

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