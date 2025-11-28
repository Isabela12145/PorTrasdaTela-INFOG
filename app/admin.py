from django.contrib import admin
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
    Ranking
)

admin.site.register(usuarios)
admin.site.register(RegistroTempoTela)
admin.site.register(DesafioOffline)
admin.site.register(Recompensa)
admin.site.register(ConquistaDesafio)
admin.site.register(ConteudoEducativo)
admin.site.register(RotinaTempoTela)
admin.site.register(Notificacao)
admin.site.register(Feedback)
admin.site.register(Diario)

@admin.register(Ponto)
class PontoAdmin(admin.ModelAdmin):
    list_display = ('usuarios', 'pontos')

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('posicao', 'usuarios', 'pontuacao_total')

