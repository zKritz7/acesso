from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Pessoa(models.Model):
    GENERO = (("M", "Masculino"), ("F", "Feminino"))
    cpf = models.CharField(max_length=11, blank=False, null=False)
    telefone = models.CharField(max_length=11, blank=True, null=True)
    genero = models.CharField(choices=GENERO, blank=False, null=True)
    data_nascimento = models.DateField(blank=False, null=False)
    nome = models.CharField(max_length=64, blank=False, null=False)

    def __str__(self):
        return self.nome
    
class Funcionario(Pessoa):
    TURNO = (("M", "Matutino"), ("V", "Vespetino"), ("N", "Noturno"))
    matricula = models.CharField(max_length=256, blank=False, null=False)
    cargo = models.CharField(max_length=256, blank=False, null=False)
    turno =  models.CharField(choices=TURNO, blank=False, null=False)
    usuario = models.OneToOneField(User, related_name='funcionario', on_delete=models.CASCADE)

class Visitante(Pessoa):
    MOTIVO = (
        ('E', 'Escola'),
        ('D', 'Delivery'),
        ('V', 'Visita técnica'),
    )

    tipo = models.CharField(max_length=1, choices=MOTIVO, blank=False, null=False)

class Endereco(models.Model):
    logradouro = models.CharField(max_length=64, blank=False, null=False)
    numero = models.CharField(max_length=8, blank=False, null=False)
    bairro = models.CharField(max_length=64, blank=False, null=False)
    cidade = models.CharField(max_length=64, blank=False, null=False)
    estado = models.CharField(max_length=64, blank=False, null=False)
    cep = models.CharField(max_length=10, blank=False, null=False)
    pessoa = models.ForeignKey(Pessoa, blank=False, null=False, on_delete=models.CASCADE, related_name='enderecos')

class Veiculo(models.Model):
    placa = models.CharField(max_length=12, blank=False, null=False)
    modelo = models.CharField(max_length=64, blank=False, null=False)
    ano = models.CharField(max_length=4, blank=False, null=False)
    cor = models.CharField(max_length=24, blank=False, null=False)
    pessoa = models.ForeignKey(Pessoa, blank=False, null=False, on_delete=models.CASCADE, related_name='veiculos')

    def __str__(self):
        return self.placa + " de " + self.pessoa.nome

class RegistroAcesso(models.Model):
    STATUS = (
        ('E', 'Em Andamento'),
        ('F', 'Finalizado'),
    )
    pessoa = models.ForeignKey(Pessoa, blank=False, null=False, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, blank=False, null=False, on_delete=models.CASCADE)
    data_hora_entrada = models.DateTimeField(blank=False, null=False)
    data_hora_saida = models.DateTimeField(blank=False, null=False)
    status = models.CharField(choices=STATUS, blank=False, null=False)

    def atualiza_status(self):
        self.status = 'F'
        self.atualiza_hora_saida(datetime.now())
        self.save

    def atualiza_hora_saida(self, hora_saida):
        self.data_hora_saida = hora_saida
        self.save