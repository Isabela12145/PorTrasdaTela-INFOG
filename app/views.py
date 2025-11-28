from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Ranking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DesafioOffline, ConquistaDesafio, RegistroTempoTela, RotinaTempoTela



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

def ranking_view(request):
    ranking = Ranking.objects.order_by('posicao')
    return render(request, 'ranking.html', {'ranking': ranking})


# --- PÁGINAS INTERNAS (proteção com login_required) ---

@login_required(login_url="login")
def alerta(request):
    return render(request, "alerta.html")


@login_required(login_url="login")
def diario(request):
    return render(request, "diario.html")


@login_required(login_url="login")
def ranking(request):
    return render(request, "ranking.html")


@login_required(login_url="login")
def recompensa(request):
    return render(request, "recompensa.html")


@login_required(login_url="login")
def profissionais(request):
    return render(request, "profissionais.html")

from .models import ConteudoEducativo

@login_required(login_url="login")
def conteudoed(request):
    conteudos = ConteudoEducativo.objects.all()
    return render(request, "conteudoed.html", {"conteudos": conteudos})

# registrar conclusão de desafio
@login_required
def concluir_desafio(request, desafio_id):
    desafio = get_object_or_404(DesafioOffline, id=desafio_id)

    # cria o registro que ativa a pontuação automática
    ConquistaDesafio.objects.create(
        usuarios=request.user.usuarios,  # seu modelo relacionado
        desafio=desafio,
        data_conclusao=timezone.now().date()
    )

    return redirect('ranking')

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

