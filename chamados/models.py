from django.contrib.auth.models import User
from django.db import models


class Chamado(models.Model):

    PRIORIDADES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]

    STATUS = [
        ('ABERTO', 'Aberto'),
        ('EM_ATENDIMENTO', 'Em atendimento'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    solicitante = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='chamados'
    )

    setor = models.CharField(max_length=100)

    comentario = models.TextField(blank=True)

    tipo = models.CharField(max_length=100)

    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default='MEDIA'
    )

    descricao = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='ABERTO'
    )

    responsavel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chamados_responsaveis'
    )

    data_abertura = models.DateTimeField(auto_now_add=True)

    data_atualizacao = models.DateTimeField(auto_now=True)

    data_conclusao = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Chamado #{self.id} - {self.solicitante.username}'


class ComentarioChamado(models.Model):

    chamado = models.ForeignKey(
        Chamado,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    mensagem = models.TextField()

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'Comentário #{self.id} - Chamado #{self.chamado.id}'

class ConfiguracaoEmail(models.Model):

    nome = models.CharField(
        max_length=100,
        default='Configuração principal'
    )

    servidor_smtp = models.CharField(
        max_length=255
    )

    porta_smtp = models.PositiveIntegerField(
        default=587
    )

    usuario_smtp = models.EmailField()

    senha_smtp = models.CharField(
        max_length=255
    )

    usar_tls = models.BooleanField(
        default=True
    )

    usar_ssl = models.BooleanField(
        default=False
    )

    email_remetente = models.EmailField()

    nome_remetente = models.CharField(
        max_length=100,
        default='Sistema de Chamados TI'
    )

    email_ti = models.EmailField(
        verbose_name='E-mail administrador TI'
    )

    ativo = models.BooleanField(
        default=True
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.nome