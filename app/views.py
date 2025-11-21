from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "index.html")

def login_page(request):
    return render(request, "login.html")

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = authenticate(request, username=email, password=senha)

        if user:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {"erro": "Login inválido!"})

def logout_user(request):
    logout(request)
    return redirect("login")


# ---- PÁGINAS INTERNAS ---- #

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
    return render(request, "profissional.html")
