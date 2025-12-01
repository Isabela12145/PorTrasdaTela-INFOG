from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DesafioOffline, ConquistaDesafio, RegistroTempoTela, RotinaTempoTela


# Adicionado para fazer a página "Desafios" funcionar
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.db import transaction
from django.db.models import F

# Página inicial
def index(request):
    return render(request, "index.html")


# Página inicial de login (GET vazio)
def login_page(request):
    return render(request, "login.html")


# LOGIN
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    error_message = None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                remember_me = request.POST.get('remember_me') == 'on'
                if not remember_me:
                    request.session.set_expiry(0)

                next_url = request.GET.get('next', 'index')
                return redirect(next_url)

        error_message = "Usuário ou senha inválidos."

    context = {
        'form': AuthenticationForm(),
        'error_message': error_message
    }
    return render(request, 'login.html', context)


# REGISTER
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# LOGOUT
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect('index')


# --- PÁGINAS INTERNAS (proteção com login_required) ---

@login_required(login_url="login")
def alerta(request):
    return render(request, "alerta.html")


@login_required(login_url="login")
def diario(request):
    return render(request, "diario.html")


@login_required(login_url="login")
def ranking(request):
    # pega os usuários ordenados por pontuação (maior → menor)
    lista = usuarios.objects.order_by("-pontos")

    ranking = []
    pos = 1

    for u in lista:
        ranking.append({
            "posicao": pos,
            "usuario": u.user.username,
            "nome": u.nome or u.user.get_full_name() or u.user.username,
            "pontos": u.pontos
        })
        pos += 1

    return render(request, "ranking.html", {"ranking": ranking})


@login_required(login_url="login")
def recompensa(request):
    return render(request, "recompensa.html")













from django.core.paginator import Paginator
@login_required(login_url="login")
def lista_profissionais(request):
    profissionais_qs = Profissional.objects.all().order_by('nome')
    per_page = 9  # ajuste para quantos mostrar por página
    paginator = Paginator(profissionais_qs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'profissionais.html', {
        'profissionais': page_obj,   # Page é iterável — conveniente para o template
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
    })













from .models import ConteudoEducativo

@login_required(login_url="login")
def conteudoed(request):
    conteudos = ConteudoEducativo.objects.all()
    return render(request, "conteudoed.html", {"conteudos": conteudos})
def conteudo_adicionar(request):
    return render(request, "conteudo_adicionar.html")


# registrar conclusão de desafio
@login_required
def desafios_view(request):
    """
    GET: renderiza a página de desafios
    POST: recebe JSON { "pontos": int, "texto": str } e atualiza usuarios.pontos,
          retorna JSON com a nova pontuação e o item do histórico
    """
    # obtém ou cria o objeto 'usuarios' associado ao usuário logado
    usuario, _ = usuarios.objects.get_or_create(
        user=request.user,
        defaults={"nome": request.user.get_full_name() or request.user.username}
    )

    if request.method == "GET":
        # renderiza template passando a pontuação atual
        return render(request, "desafios.html", {"usuario": usuario})

    # POST: aceitar JSON ou form-encoded
    try:
        if request.content_type == "application/json":
            payload = json.loads(request.body.decode("utf-8") or "{}")
            pontos = int(payload.get("pontos", 0))
            texto = str(payload.get("texto", "")).strip()
        else:
            # fallback para form POST
            pontos = int(request.POST.get("pontos", 0))
            texto = request.POST.get("texto", "").strip()
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Valor de pontos inválido.")

    if pontos <= 0:
        return HttpResponseBadRequest("Pontos devem ser um valor inteiro maior que zero.")

    # atualiza de forma atômica usando F() para evitar race conditions
    with transaction.atomic():
        usuarios.objects.filter(pk=usuario.pk).update(pontos=F("pontos") + pontos)
        usuario.refresh_from_db()  # garante valor atualizado

    # resposta que o front usará para atualizar UI
    return JsonResponse({
        "success": True,
        "novo_total": usuario.pontos,
        "item": {
            "texto": texto or f"{pontos} pontos",
            "pontos": pontos
        }
    })

@login_required
def registrar_tempo_tela(request):
    if request.method == "POST":
        minutos = int(request.POST.get("minutos"))

        RegistroTempoTela.objects.create(
            usuarios=request.user.usuarios,
            minutos_uso=minutos,
            data=timezone.now().date()
        )

        return redirect("ranking")

    return render(request, "registro_tempo.html")




