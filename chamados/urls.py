from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path(
        'chamados/novo/',
        views.abrir_chamado,
        name='abrir_chamado'
    ),

    path(
        'chamados/',
        views.meus_chamados,
        name='meus_chamados'
    ),
]