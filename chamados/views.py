from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Chamado
from .forms import (
    ChamadoForm,
    ComentarioForm,
    StatusChamadoForm,
    ResponsavelChamadoForm
)
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.views import LoginView

def usuario_eh_ti(user):
    return user.groups.filter(name='TI').exists()

def redirecionar_apos_login(request):

    if usuario_eh_ti(request.user):
        return redirect('central_ti')

    return redirect('home')

class LoginUsuarioView(LoginView):

    template_name = 'registration/login.html'

    def get_success_url(self):

        if usuario_eh_ti(self.request.user):
            return '/central-ti/'

        return '/'

@login_required
def home(request):
    return render(request, 'chamados/home.html')


@login_required
def abrir_chamado(request):

    if request.method == 'POST':
        form = ChamadoForm(request.POST)

        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.solicitante = request.user
            chamado.save()

            if usuario_eh_ti(request.user):
                return redirect('central_ti')

            return redirect('home')

    else:
        form = ChamadoForm()

    return render(
        request,
        'chamados/abrir_chamado.html',
        {
            'form': form,
            'is_ti': usuario_eh_ti(request.user),
        }
    )


@login_required
def meus_chamados(request):

    if usuario_eh_ti(request.user):

        chamados = Chamado.objects.all().order_by('-data_abertura')

    else:

        chamados = Chamado.objects.filter(
            solicitante=request.user
        ).order_by('-data_abertura')

    return render(
        request,
        'chamados/meus_chamados.html',
        {'chamados': chamados}
    )

@login_required
def detalhe_chamado(request, id):

    if usuario_eh_ti(request.user):

        chamado = Chamado.objects.get(
            id=id
        )

    else:

        chamado = Chamado.objects.get(
            id=id,
            solicitante=request.user
        )

    comentarios = chamado.comentarios.all().order_by('data_criacao')

    if request.method == 'POST':

        # Alteração de responsável pelo TI
        if usuario_eh_ti(request.user) and 'responsavel' in request.POST:

            form_responsavel = ResponsavelChamadoForm(
                request.POST,
                instance=chamado
            )

            if form_responsavel.is_valid():

                form_responsavel.save()

                return redirect(
                    'detalhe_chamado',
                    id=chamado.id
                )

        # Alteração de status pelo TI
        elif usuario_eh_ti(request.user) and 'status' in request.POST:

            form_status = StatusChamadoForm(
                request.POST,
                instance=chamado
            )

            if form_status.is_valid():

                chamado = form_status.save(commit=False)

                if chamado.status == 'CONCLUIDO':

                    from django.utils import timezone

                    chamado.data_conclusao = timezone.now()

                else:

                    chamado.data_conclusao = None

                chamado.save()

                return redirect(
                    'detalhe_chamado',
                    id=chamado.id
                )

        # Adição de comentário
        else:

            form = ComentarioForm(request.POST)

            if form.is_valid():

                comentario = form.save(commit=False)

                comentario.chamado = chamado
                comentario.usuario = request.user

                comentario.save()

                return redirect(
                    'detalhe_chamado',
                    id=chamado.id
                )

    else:

        form = ComentarioForm()

    form_status = StatusChamadoForm(
        instance=chamado
    )

    form_responsavel = ResponsavelChamadoForm(
        instance=chamado
    )

    return render(
        request,
        'chamados/detalhe_chamado.html',
        {
            'chamado': chamado,
            'comentarios': comentarios,
            'form': form,
            'form_status': form_status,
            'form_responsavel': form_responsavel,
            'is_ti': usuario_eh_ti(request.user),
        }
    )

@login_required
def central_ti(request):

    if not usuario_eh_ti(request.user):
        return redirect('home')

    total_abertos = Chamado.objects.filter(
        status='ABERTO'
    ).count()

    total_em_atendimento = Chamado.objects.filter(
        status='EM_ATENDIMENTO'
    ).count()

    total_concluidos = Chamado.objects.filter(
        status='CONCLUIDO'
    ).count()

    total_urgentes = Chamado.objects.filter(
        prioridade='URGENTE'
    ).count()

    chamados_recentes = Chamado.objects.select_related(
        'solicitante',
        'responsavel'
    ).order_by(
        '-data_abertura'
    )

    # =========================
    # FILTRO POR STATUS
    # =========================

    status_filtro = request.GET.get('status')

    if status_filtro:
        chamados_recentes = chamados_recentes.filter(
            status=status_filtro
        )

    # =========================
    # FILTRO POR PRIORIDADE
    # =========================

    prioridade_filtro = request.GET.get('prioridade')

    if prioridade_filtro:
        chamados_recentes = chamados_recentes.filter(
            prioridade=prioridade_filtro
        )

    # =========================
    # FILTRO POR TIPO
    # =========================

    tipo_filtro = request.GET.get('tipo')

    if tipo_filtro:
        chamados_recentes = chamados_recentes.filter(
            tipo=tipo_filtro
        )

    # =========================
    # FILTRO POR SETOR
    # =========================

    setor_filtro = request.GET.get('setor')

    if setor_filtro:
        chamados_recentes = chamados_recentes.filter(
            setor=setor_filtro
        )

    # =========================
    # FILTRO POR RESPONSÁVEL
    # =========================

    responsavel_filtro = request.GET.get('responsavel')

    if responsavel_filtro:
        chamados_recentes = chamados_recentes.filter(
            responsavel_id=responsavel_filtro
        )

    # Limita aos 10 mais recentes
    # somente depois dos filtros

    # =========================
    # BUSCA
    # =========================

    busca = request.GET.get('busca', '').strip()

    if busca:
        filtros_busca = Q(
            descricao__icontains=busca
        ) | Q(
            solicitante__username__icontains=busca
        ) | Q(
            solicitante__first_name__icontains=busca
        ) | Q(
            solicitante__last_name__icontains=busca
        ) | Q(
            tipo__icontains=busca
        )

        if busca.isdigit():
            filtros_busca |= Q(
                id=int(busca)
            )

        chamados_recentes = chamados_recentes.filter(
            filtros_busca
        )

    chamados_recentes = chamados_recentes[:10]

    responsaveis_ti = User.objects.filter(
        groups__name='TI'
    ).order_by(
        'first_name',
        'username'
    )

    return render(
        request,
        'chamados/central_ti.html',
        {
            'total_abertos': total_abertos,
            'total_em_atendimento': total_em_atendimento,
            'total_concluidos': total_concluidos,
            'total_urgentes': total_urgentes,
            'chamados_recentes': chamados_recentes,
            'setor_filtro': setor_filtro,
            'status_filtro': status_filtro,
            'prioridade_filtro': prioridade_filtro,
            'tipo_filtro': tipo_filtro,
            'responsavel_filtro': responsavel_filtro,
            'busca': busca,
        }
    )