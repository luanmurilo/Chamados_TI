from django import forms
from .models import Chamado, ComentarioChamado
from django.contrib.auth.models import User

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
            'descricao',
        ]

        widgets = {
            'prioridade': forms.Select(),

            'descricao': forms.Textarea(attrs={
                'placeholder': 'Descreva detalhadamente o problema',
                'rows': 6
            }),
        }


class ComentarioForm(forms.ModelForm):

    class Meta:
        model = ComentarioChamado

        fields = [
            'mensagem',
        ]

        widgets = {
            'mensagem': forms.Textarea(attrs={
                'placeholder': 'Digite sua mensagem...',
                'rows': 4,
            }),
        }

class StatusChamadoForm(forms.ModelForm):

    class Meta:
        model = Chamado

        fields = [
            'status',
        ]

        widgets = {
            'status': forms.Select(),
        }

class ResponsavelChamadoForm(forms.ModelForm):

    class Meta:
        model = Chamado

        fields = [
            'responsavel',
        ]

        widgets = {
            'responsavel': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['responsavel'].queryset = User.objects.filter(
            groups__name='TI'
        ).order_by('first_name', 'username')

        self.fields['responsavel'].empty_label = 'Ainda não atribuído'