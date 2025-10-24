from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('usuarios/', TemplateView.as_view(template_name='usuarios.html'), name='usuarios'),
    path('criancas/', TemplateView.as_view(template_name='criancas.html'), name='criancas'),
    path('registros-tempo-tela/', TemplateView.as_view(template_name='registros-tempo-tela.html'), name='registros-tempo-tela'),
    path('desafios-offline/', TemplateView.as_view(template_name='desafios-offline.html'), name='desafios-offline'),
    path('recompensas/', TemplateView.as_view(template_name='recompensas.html'), name='recompensas'),
    path('conteudos-educativos/', TemplateView.as_view(template_name='conteudos-educativos.html'), name='conteudos-educativos'),
    path('feedback/', TemplateView.as_view(template_name='feedback.html'), name='feedback'),
]
