from django.db import models


class Paciente(models.Model):
    GENERO_CHOICES = [
        ('feminino', 'Feminino'),
        ('masculino', 'Masculino'),
        ('outro', 'Outro'),
    ]

    ESPECIALIDADE_CHOICES = [
        ('nutricionista_geral', 'Nutricionista Geral'),
        ('nutricionista_infantil', 'Nutricionista Infantil'),
        ('introducao_alimentar', 'Introdução Alimentar'),
        ('fisioterapia_geral', 'Fisioterapia Geral'),
        ('fisioterapia_infantil', 'Fisioterapia Infantil'),
    ]

    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    especialidade = models.CharField(max_length=50, choices=ESPECIALIDADE_CHOICES)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    data_consulta = models.DateField()
    hora_desejada = models.TimeField()
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class NutricionistaGeral(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    nome_paciente = models.CharField(max_length=255)
    observacao = models.TextField(blank=True)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    data_consulta = models.DateField()  # Novo campo
    hora_desejada = models.TimeField()  # Novo campo

    def __str__(self):
        return self.nome


class NutricionistaInfantil(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    nome_paciente = models.CharField(max_length=255)
    observacao = models.TextField(blank=True)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    data_consulta = models.DateField()  # Novo campo
    hora_desejada = models.TimeField()  # Novo campo
    
    def __str__(self):
        return self.nome


class IntroducaoAlimentar(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    nome_paciente = models.CharField(max_length=255)
    observacao = models.TextField(blank=True)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    data_consulta = models.DateField()  # Novo campo
    hora_desejada = models.TimeField()  # Novo campo

    def __str__(self):
        return self.nome


class FisioterapiaGeral(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    nome_paciente = models.CharField(max_length=255)
    observacao = models.TextField(blank=True)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    data_consulta = models.DateField()  # Novo campo
    hora_desejada = models.TimeField()  # Novo campo

    def __str__(self):
        return self.nome


class FisioterapiaInfantil(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    nome_paciente = models.CharField(max_length=255)
    observacao = models.TextField(blank=True)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    data_consulta = models.DateField()  # Novo campo
    hora_desejada = models.TimeField()  # Novo campo

    def __str__(self):
        return self.nome
    





