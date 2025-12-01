from django.contrib import admin
from .models import Profissional
from .models import (
    usuarios,
    RegistroTempoTela,
    DesafioOffline,
    Recompensa,
    ConquistaDesafio,
    ConteudoEducativo,
    RotinaTempoTela,
    Notificacao,
    Feedback,
    Diario,
    Ponto,
    Ranking,
    Profissional,
)

# Modelos simples — registrados diretamente
admin.site.register(usuarios)
admin.site.register(RegistroTempoTela)
admin.site.register(DesafioOffline)
admin.site.register(Recompensa)
admin.site.register(ConquistaDesafio)
admin.site.register(RotinaTempoTela)
admin.site.register(Notificacao)
admin.site.register(Feedback)
admin.site.register(Diario)

# Modelos com configurações personalizadas



from django.contrib import admin
from .models import ConteudoEducativo

@admin.register(ConteudoEducativo)
class ConteudoEducativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'profissionalAutor')
    search_fields = ('titulo', 'descricao', 'profissionalAutor__nome')
    list_filter = ('tipo',)




@admin.register(Ponto)
class PontoAdmin(admin.ModelAdmin):
    list_display = ("usuarios", "pontos")
    search_fields = ("usuarios__username",)


@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ("posicao", "usuarios", "pontuacao_total")
    search_fields = ("usuarios__username",)
    ordering = ("posicao",)


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ("nome", "especialidade")
