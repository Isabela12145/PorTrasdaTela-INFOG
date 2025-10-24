from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def usuarios(request):
    return render(request, 'usuarios.html')

def criancas(request):
    return render(request, 'criancas.html')

def registros_tempo_tela(request):
    return render(request, 'registros-tempo-tela.html')

def desafios_offline(request):
    return render(request, 'desafios-offline.html')

def recompensas(request):
    return render(request, 'recompensas.html')

def conteudos_educativos(request):
    return render(request, 'conteudos-educativos.html')

def feedback(request):
    return render(request, 'feedback.html')
