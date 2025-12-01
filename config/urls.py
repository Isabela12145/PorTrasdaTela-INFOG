from django.contrib import admin
from django.urls import path
from app import views
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas principais
    path('', views.index, name="index"),
    path('alerta/', views.alerta, name="alerta"),
    path('diario/', views.diario, name="diario"),
    path('ranking/', views.ranking, name="ranking"),
    path('recompensa/', views.recompensa, name="recompensa"),
    
    path('profissionais/', views.lista_profissionais, name='profissionais'),

    path('conteudoed/', views.conteudoed, name="conteudoed"),
    path("desafios/", views.desafios_view, name="desafios"),
    path("tempo/registrar/", views.registrar_tempo_tela, name="registrar_tempo_tela"),

    # Autenticação
    path('login/', views.login_view, name='login'),      # CORRIGIDO: adicionado views.
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # Conteúdo educativo
    path('conteudo/adicionar/', views.conteudo_adicionar, name='conteudo_adicionar'),

    # Login pages (se tiver separado)
    path('login-page/', views.login_page, name='login_page'),
    
    
]