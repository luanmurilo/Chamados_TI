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

    setor = models.CharField(
        max_length=100
    )

    comentario = models.TextField(
        blank=True
    )

    tipo = models.CharField(
        max_length=100
    )

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

    responsavel = models.CharField(
        max_length=150,
        blank=True
    )

    data_abertura = models.DateTimeField(
        auto_now_add=True
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    data_conclusao = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Chamado #{self.id} - {self.solicitante.username}'

