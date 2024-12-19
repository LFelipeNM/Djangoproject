from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Paciente, NutricionistaGeral, NutricionistaInfantil, IntroducaoAlimentar, FisioterapiaGeral, FisioterapiaInfantil

@receiver(post_save, sender=Paciente)
def create_specialty_record(sender, instance, created, **kwargs):
    if created:
        if instance.especialidade == 'nutricionista_geral':
            NutricionistaGeral.objects.create(
                paciente=instance,
                nome_paciente=instance.nome,  
                observacao=instance.observacoes,
                data_consulta=instance.data_consulta,  
                hora_desejada=instance.hora_desejada  
            )
        elif instance.especialidade == 'nutricionista_infantil':
            NutricionistaInfantil.objects.create(
                paciente=instance,
                nome_paciente=instance.nome,
                observacao=instance.observacoes,
                data_consulta=instance.data_consulta,  
                hora_desejada=instance.hora_desejada  
            )
        elif instance.especialidade == 'introducao_alimentar':
            IntroducaoAlimentar.objects.create(
                paciente=instance,
                nome_paciente=instance.nome,
                observacao=instance.observacoes,
                data_consulta=instance.data_consulta,  
                hora_desejada=instance.hora_desejada  
            )
        elif instance.especialidade == 'fisioterapia_geral':
            FisioterapiaGeral.objects.create(
                paciente=instance,
                nome_paciente=instance.nome,
                observacao=instance.observacoes,
                data_consulta=instance.data_consulta,  
                hora_desejada=instance.hora_desejada  
            )
        elif instance.especialidade == 'fisioterapia_infantil':
            FisioterapiaInfantil.objects.create(
                paciente=instance,
                nome_paciente=instance.nome,
                observacao=instance.observacoes,
                data_consulta=instance.data_consulta,  
                hora_desejada=instance.hora_desejada  
            )
