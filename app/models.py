from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Usuário
from django.core.validators import RegexValidator

class usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)
    telefone = models.CharField(
        max_length=15,
        verbose_name="Telefone",
        validators=[RegexValidator(r'^\+?\d{10,15}$', "Número de telefone inválido")]
    )

    # Além desses dados, o usuário também tem o dado username que é herdado de User

    # Campos caso o tipo do usuário for funcionário
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name="CPF")

    pontos = models.IntegerField(default=0, verbose_name="Pontos")

    def __str__(self):  # CORRIGIDO: dois underscores
        return self.nome or self.user.username

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

class RegistroTempoTela(models.Model):
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, verbose_name="Usuario")
    data = models.DateField(verbose_name="Data do registro")
    minutos_uso = models.IntegerField(verbose_name="Minutos de uso")

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"{self.usuarios.nome} - {self.data}"

    class Meta:
        verbose_name = "Registro de Tempo de Tela"
        verbose_name_plural = "Registros de Tempo de Tela"


class DesafioOffline(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título do desafio")
    descricao = models.TextField(verbose_name="Descrição")
    nivel_dificuldade = models.CharField(max_length=50, verbose_name="Nível de dificuldade")
    pontos_recompensa = models.IntegerField(verbose_name="Pontos de recompensa")

    def __str__(self):  # CORRIGIDO: dois underscores
        return self.titulo

    class Meta:
        verbose_name = "Desafio Offline"
        verbose_name_plural = "Desafios Offline"


class Recompensa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da recompensa")
    descricao = models.TextField(verbose_name="Descrição")
    pontos_necessarios = models.IntegerField(verbose_name="Pontos necessários para desbloquear")

    def __str__(self):  # CORRIGIDO: dois underscores
        return self.nome

    class Meta:
        verbose_name = "Recompensa"
        verbose_name_plural = "Recompensas"


class ConquistaDesafio(models.Model):
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, verbose_name="Usuario")
    desafio = models.ForeignKey(DesafioOffline, on_delete=models.CASCADE, verbose_name="Desafio")
    data_conclusao = models.DateField(verbose_name="Data da conclusão")

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"{self.usuarios.nome} - {self.desafio.titulo}"  # CORRIGIDO: self.usuarios (não self.usuario)

    class Meta:
        verbose_name = "Conquista de Desafio"
        verbose_name_plural = "Conquistas de Desafios"

















import hashlib
import urllib.parse
from urllib.parse import urlparse, parse_qs

from django.db import models
from django.utils.text import Truncator
from django.utils.safestring import mark_safe


class Profissional(models.Model):
    nome = models.CharField("Nome", max_length=200)
    especialidade = models.CharField("Especialidade / Área", max_length=200, blank=True)
    descricao = models.TextField("Descrição", blank=True)
    foto_url = models.URLField(
        "URL da Foto",
        max_length=500,
        blank=True,
        help_text="Coloque uma URL pública (http(s)) apontando para a imagem do profissional"
    )

    def __str__(self):
        return self.nome or ""

    def _initials(self):
        if not self.nome:
            return "?"
        parts = [p for p in self.nome.strip().split() if p]
        if not parts:
            return "?"
        if len(parts) == 1:
            return (parts[0][0] if parts[0] else "?").upper()
        return (parts[0][0] + parts[-1][0]).upper()

    def _bg_color_from_name(self):
        if not self.nome:
            return "#999999"
        h = hashlib.md5(self.nome.encode("utf-8")).hexdigest()
        return f"#{h[:6]}"

    @property
    def avatar_src(self):
        """
        Retorna a URL da foto (se existir) ou um data:image/svg+xml;utf8,... com as iniciais.
        Se retornar data-url (svg), marcamos como safe para evitar escape que quebre a url.
        """
        if self.foto_url:
            return self.foto_url

        initials = self._initials()
        bg = self._bg_color_from_name()
        text_color = "#ffffff"
        size = 200

        svg = (
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}' viewBox='0 0 {size} {size}'>"
            f"<rect width='100%' height='100%' fill='{bg}'/>"
            f"<text x='50%' y='50%' font-family='Poppins, Arial, sans-serif' "
            f"font-size='{int(size*0.42)}' fill='{text_color}' dominant-baseline='middle' text-anchor='middle'>{initials}</text>"
            f"</svg>"
        )
        data_url = "data:image/svg+xml;utf8," + urllib.parse.quote(svg)
        return mark_safe(data_url)


class ConteudoEducativo(models.Model):
    TIPOS = [
        ('texto', 'Texto'),
        ('video', 'Vídeo'),
        ('imagem', 'Imagem'),
    ]

    titulo = models.CharField(max_length=100, verbose_name="Título")
    tipo = models.CharField(max_length=10, choices=TIPOS, verbose_name="Tipo de conteúdo")
    arquivo_url = models.URLField(verbose_name="URL do conteúdo")
    descricao = models.TextField(verbose_name="Descrição")

    profissionalAutor = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        related_name='conteudos',
        verbose_name='Autor (Profissional)'
    )

    def save(self, *args, **kwargs):
        # Se for vídeo do YouTube, extrai o ID e remove parâmetros
        if self.tipo == "video" and self.arquivo_url:
            url = self.arquivo_url.strip()

            # se já recebeu apenas um id, mantemos
            if ("youtube" not in url and "youtu.be" not in url and '/' not in url) and len(url) <= 50:
                video_id = url
            else:
                if "watch?v=" in url:
                    video_id = url.split("watch?v=")[-1]
                elif "youtu.be/" in url:
                    video_id = url.split("youtu.be/")[-1]
                elif "shorts/" in url:
                    video_id = url.split("shorts/")[-1]
                else:
                    parsed = urlparse(url)
                    qs = parse_qs(parsed.query)
                    video_id = qs.get('v', [url])[-1]

            # Remove parâmetros como '?si=' ou '&ab_channel='
            if "?" in video_id:
                video_id = video_id.split("?")[0]
            if "&" in video_id:
                video_id = video_id.split("&")[0]

            self.arquivo_url = video_id

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo or ""

    # excerpt como property sem parâmetros (uso direto no template: {{ c.excerpt }})
    @property
    def excerpt(self):
        return Truncator(self.descricao or "").chars(120)

    def _extract_video_id(self, value):
        """Extrai o video id de um valor que pode ser um id puro ou uma URL do YouTube."""
        if not value:
            return None
        v = value.strip()

        # já é apenas um id curto (sem '/' ou 'youtu' e razoável em comprimento)
        if ("youtube" not in v and "youtu.be" not in v and '/' not in v) and len(v) <= 50:
            return v

        # vários formatos possíveis
        if "watch?v=" in v:
            vid = v.split("watch?v=")[-1]
        elif "youtu.be/" in v:
            vid = v.split("youtu.be/")[-1]
        elif "shorts/" in v:
            vid = v.split("shorts/")[-1]
        else:
            parsed = urlparse(v)
            qs = parse_qs(parsed.query)
            vid = qs.get('v', [v])[-1]

        # remove quaisquer parâmetros residuais
        if "?" in vid:
            vid = vid.split("?")[0]
        if "&" in vid:
            vid = vid.split("&")[0]

        return vid or None

    @property
    def video_id(self):
        """Retorna o id do vídeo caso tipo == 'video' — funciona tanto se arquivo_url for id ou URL."""
        if self.tipo != 'video' or not self.arquivo_url:
            return None
        return self._extract_video_id(self.arquivo_url)

    @property
    def youtube_watch_url(self):
        """URL do YouTube (watch) — usa o id extraído quando disponível, senão retorna arquivo_url."""
        vid = self.video_id
        if vid:
            return f"https://www.youtube.com/watch?v={vid}"
        return self.arquivo_url or None

    @property
    def youtube_embed_url(self):
        """URL para usar no iframe embed — retorna None se não houver id."""
        vid = self.video_id
        return f"https://www.youtube.com/embed/{vid}" if vid else None

    @property
    def youtube_thumbnail(self):
        """Thumbnail do YouTube (preview)."""
        vid = self.video_id
        return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else None

















class RotinaTempoTela(models.Model):
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, verbose_name="Usuario")
    limite_diario_minutos = models.IntegerField(verbose_name="Limite diário (minutos)")
    atividades_offline_planejadas = models.TextField(verbose_name="Atividades offline planejadas")

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"Rotina de {self.usuarios.nome}"

    class Meta:
        verbose_name = "Rotina de Tempo de Tela"
        verbose_name_plural = "Rotinas de Tempo de Tela"


class Notificacao(models.Model):
    usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE, verbose_name="Usuário")
    mensagem = models.TextField(verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de envio")
    lida = models.BooleanField(default=False, verbose_name="Lida")

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"Notificação para {self.usuario.nome}"

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"


class Feedback(models.Model):
    usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE, verbose_name="Usuário")
    mensagem = models.TextField(verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de envio")

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"Feedback de {self.usuario.nome}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"


class Diario(models.Model):
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, verbose_name="Criança")
    data = models.DateField(verbose_name="Data do registro")
    atividade_realizada = models.TextField(verbose_name="Atividade realizada")
    tempo_tela_utilizado = models.IntegerField(verbose_name="Tempo de tela utilizado (minutos)")
    reflexao = models.TextField(blank=True, verbose_name="Reflexão do dia")

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"Diário de {self.usuarios.nome} - {self.data}"

    class Meta:
        verbose_name = "Diário"
        verbose_name_plural = "Diários"


class Alerta(models.Model):
    TIPOS_ALERTA = [
        ('limite_excedido', 'Limite de Tela Excedido'),
        ('desafio_disponivel', 'Desafio Disponível'),
        ('recompensa_disponivel', 'Recompensa Disponível'),
    ]
    
    usuarios = models.ForeignKey(usuarios, on_delete=models.CASCADE, verbose_name="Criança")
    tipo = models.CharField(max_length=50, choices=TIPOS_ALERTA, verbose_name="Tipo de alerta")
    mensagem = models.TextField(verbose_name="Mensagem do alerta")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    lido = models.BooleanField(default=False, verbose_name="Lido")

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"Alerta para {self.usuarios.nome} - {self.tipo}"

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"

# -----------------------------------
# MODELS DO SISTEMA DE PONTUAÇÃO
# -----------------------------------

class Ponto(models.Model):
    usuarios = models.OneToOneField(usuarios, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"{self.usuarios.nome} - {self.pontos} pts"  # CORRIGIDO: self.usuarios.nome

class Ranking(models.Model):
    usuarios = models.OneToOneField(usuarios, on_delete=models.CASCADE)
    posicao = models.PositiveIntegerField(default=0)
    pontuacao_total = models.IntegerField(default=0)

    class Meta:
        ordering = ['posicao']  # sempre retorna ordenado

    def __str__(self):  # CORRIGIDO: dois underscores
        return f"{self.posicao}º - {self.usuarios.nome} ({self.pontuacao_total} pts)"  # CORRIGIDO: self.usuarios.nome


