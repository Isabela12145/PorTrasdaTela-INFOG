from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator






# Usuário
from django.core.validators import RegexValidator

class Usuario(models.Model):
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

    def __str__(self):
        return self.nome or self.user.username

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"













class Crianca(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da criança")
    data_nasc = models.DateField(verbose_name="Data de nascimento")
    tempo_tela_diario = models.IntegerField(verbose_name="Tempo de tela diário (minutos)")
    vinculo_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Responsável")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Criança"
        verbose_name_plural = "Crianças"


class RegistroTempoTela(models.Model):
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, verbose_name="Criança")
    data = models.DateField(verbose_name="Data do registro")
    minutos_uso = models.IntegerField(verbose_name="Minutos de uso")

    def __str__(self):
        return f"{self.crianca.nome} - {self.data}"

    class Meta:
        verbose_name = "Registro de Tempo de Tela"
        verbose_name_plural = "Registros de Tempo de Tela"


class DesafioOffline(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título do desafio")
    descricao = models.TextField(verbose_name="Descrição")
    nivel_dificuldade = models.CharField(max_length=50, verbose_name="Nível de dificuldade")
    pontos_recompensa = models.IntegerField(verbose_name="Pontos de recompensa")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Desafio Offline"
        verbose_name_plural = "Desafios Offline"


class Recompensa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da recompensa")
    descricao = models.TextField(verbose_name="Descrição")
    pontos_necessarios = models.IntegerField(verbose_name="Pontos necessários para desbloquear")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Recompensa"
        verbose_name_plural = "Recompensas"


class ConquistaDesafio(models.Model):
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, verbose_name="Criança")
    desafio = models.ForeignKey(DesafioOffline, on_delete=models.CASCADE, verbose_name="Desafio")
    data_conclusao = models.DateField(verbose_name="Data da conclusão")

    def __str__(self):
        return f"{self.crianca.nome} - {self.desafio.titulo}"

    class Meta:
        verbose_name = "Conquista de Desafio"
        verbose_name_plural = "Conquistas de Desafios"


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

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Conteúdo Educativo"
        verbose_name_plural = "Conteúdos Educativos"


class RotinaTempoTela(models.Model):
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, verbose_name="Criança")
    limite_diario_minutos = models.IntegerField(verbose_name="Limite diário (minutos)")
    atividades_offline_planejadas = models.TextField(verbose_name="Atividades offline planejadas")

    def __str__(self):
        return f"Rotina de {self.crianca.nome}"

    class Meta:
        verbose_name = "Rotina de Tempo de Tela"
        verbose_name_plural = "Rotinas de Tempo de Tela"


class Notificacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    mensagem = models.TextField(verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de envio")
    lida = models.BooleanField(default=False, verbose_name="Lida")

    def __str__(self):
        return f"Notificação para {self.usuario.nome}"

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"


class Feedback(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    mensagem = models.TextField(verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de envio")

    def __str__(self):
        return f"Feedback de {self.usuario.nome}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"


class Ponto(models.Model):
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, verbose_name="Criança")
    pontos = models.IntegerField(default=0, verbose_name="Pontos acumulados")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")

    def __str__(self):
        return f"Pontos de {self.crianca.nome}: {self.pontos}"

    class Meta:
        verbose_name = "Ponto"
        verbose_name_plural = "Pontos"


class Ranking(models.Model):
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, verbose_name="Criança")
    posicao = models.IntegerField(verbose_name="Posição no ranking")
    pontuacao_total = models.IntegerField(verbose_name="Pontuação total")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")

    def __str__(self):
        return f"{self.crianca.nome} - Posição {self.posicao}"

    class Meta:
        verbose_name = "Ranking"
        verbose_name_plural = "Rankings"


class Diario(models.Model):
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, verbose_name="Criança")
    data = models.DateField(verbose_name="Data do registro")
    atividade_realizada = models.TextField(verbose_name="Atividade realizada")
    tempo_tela_utilizado = models.IntegerField(verbose_name="Tempo de tela utilizado (minutos)")
    reflexao = models.TextField(blank=True, verbose_name="Reflexão do dia")

    def __str__(self):
        return f"Diário de {self.crianca.nome} - {self.data}"

    class Meta:
        verbose_name = "Diário"
        verbose_name_plural = "Diários"


class Alerta(models.Model):
    TIPOS_ALERTA = [
        ('limite_excedido', 'Limite de Tela Excedido'),
        ('desafio_disponivel', 'Desafio Disponível'),
        ('recompensa_disponivel', 'Recompensa Disponível'),
    ]
    
    crianca = models.ForeignKey(Crianca, on_delete=models.CASCADE, verbose_name="Criança")
    tipo = models.CharField(max_length=50, choices=TIPOS_ALERTA, verbose_name="Tipo de alerta")
    mensagem = models.TextField(verbose_name="Mensagem do alerta")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    lido = models.BooleanField(default=False, verbose_name="Lido")

    def __str__(self):
        return f"Alerta para {self.crianca.nome} - {self.tipo}"

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"