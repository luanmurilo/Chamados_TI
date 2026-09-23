from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ChamadoForm, ComentarioForm
from .forms import ChamadoForm
from .models import Chamado

def usuario_eh_ti(user):
    return user.groups.filter(name='TI').exists()

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

            return redirect('home')

    else:
        form = ChamadoForm()

    return render(
        request,
        'chamados/abrir_chamado.html',
        {'form': form}
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

    return render(
        request,
        'chamados/detalhe_chamado.html',
        {
            'chamado': chamado,
            'comentarios': comentarios,
            'form': form,
        }
    )