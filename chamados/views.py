from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ChamadoForm
from .models import Chamado


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
    chamados = Chamado.objects.filter(
        solicitante=request.user
    ).order_by('-data_abertura')

    return render(
        request,
        'chamados/meus_chamados.html',
        {'chamados': chamados}
    )