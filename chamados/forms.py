from django import forms
from .models import Chamado


class ChamadoForm(forms.ModelForm):

    SETORES = [
        ('TI', 'TI'),
        ('RH', 'RH'),
        ('ENG_APLICADA', 'ENG APLICADA'),
        ('LOGISTICA', 'LOGÍSTICA'),
        ('MARKETING', 'MARKETING'),
        ('FINANCEIRO', 'FINANCEIRO'),
        ('JURIDICO', 'JURÍDICO'),
        ('DIRETORIA', 'DIRETORIA'),
        ('POS_OBRA', 'PÓS OBRA'),
        ('ALMOXARIFADO', 'ALMOXARIFADO'),
        ('SHOWROOM', 'SHOWROOM'),
        ('SUPRIMENTOS', 'SUPRIMENTOS'),
        ('PROJETOS', 'PROJETOS'),
        ('ARQUITETURA', 'ARQUITETURA'),
        ('QSM', 'QSM'),
        ('OUTROS', 'OUTROS'),
    ]

    TIPOS = [
        ('OFFICE', 'Office'),
        ('IMPRESSORA', 'Impressora'),
        ('MUDANCA', 'Mudança'),
        ('PC', 'PC'),
        ('SOFTWARE', 'Software'),
        ('DRIVE', 'Drive'),
        ('EMAIL', 'E-mail'),
        ('PERIFERICOS', 'Periféricos'),
        ('OUTROS', 'Outros'),
    ]

    setor = forms.ChoiceField(
        choices=SETORES,
        label='Setor'
    )

    tipo = forms.ChoiceField(
        choices=TIPOS,
        label='Tipo'
    )

    class Meta:
        model = Chamado

        fields = [
            'setor',
            'tipo',
            'prioridade',
            'comentario',
            'descricao',
        ]

        widgets = {
            'prioridade': forms.Select(),

            'comentario': forms.Textarea(attrs={
                'placeholder': 'Adicione um comentário, se necessário',
                'rows': 3
            }),

            'descricao': forms.Textarea(attrs={
                'placeholder': 'Descreva detalhadamente o problema',
                'rows': 6
            }),
        }