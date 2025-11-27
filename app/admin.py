from django.contrib import admin
from .models import (
    Usuario,
    Crianca,
    RegistroTempoTela,
    DesafioOffline,
    Recompensa,
    ConquistaDesafio,
    ConteudoEducativo,
    RotinaTempoTela,
    Notificacao,
    Feedback,
)

admin.site.register(Usuario)
admin.site.register(Crianca)
admin.site.register(RegistroTempoTela)
admin.site.register(DesafioOffline)
admin.site.register(Recompensa)
admin.site.register(ConquistaDesafio)
admin.site.register(ConteudoEducativo)
admin.site.register(RotinaTempoTela)
admin.site.register(Notificacao)
admin.site.register(Feedback)
