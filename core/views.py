from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from .forms import UserRegistrationForm, PacienteForm
from .models import NutricionistaGeral, NutricionistaInfantil, IntroducaoAlimentar, FisioterapiaGeral, FisioterapiaInfantil, Paciente
from twilio.rest import Client  
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect



def home(request):
    return render(request, 'home.html')


def login_page(request):
    return render(request, 'login.html')


def carregamento(request):
    return render(request, 'carregamento.html')


def loginerro(request):
    return render(request, 'loginERRO.html')


def agendamento(request):
    return render(request, 'agendamento_form.html')


def carregamento2(request):
    return render(request, 'carregamento2.html')


def carregamento3(request):
    return render(request, 'carregamento3.html')


def carregamento4(request):
    return render(request, 'carregamento4.html')


def carregamento5(request):
    return render(request, 'carregamento5.html')


def verconsultas(request):
    return render(request, 'agendamento_list.html')


def cadastro(request):
    return render(request, 'cadastro.html')


def home_logado(request):
    return render(request, 'home_logado.html')


def home_logadoM(request):
    return render(request, 'home_logadoM.html')


def cpfjaexiste(request):
    return render(request, 'cadastroCPFERRO.html')


def senhasdiferentes(request):
    return render(request, 'cadastroSENHAIGUAIS.html')


def register(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        celular = request.POST.get('celular')
        data_nascimento = request.POST.get('data_nascimento')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirme_senha = request.POST.get('confirme_senha')
        sexo = request.POST.get('sexo')

        if senha != confirme_senha:
            return redirect('senhaerradas')

        if User.objects.filter(email=email).exists():
            return redirect('emailjaexiste')

        primeiro_nome = nome.split()[0]
        username = primeiro_nome
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{primeiro_nome}{counter}"
            counter += 1

        if User.objects.filter(username=username).exists():
            unique_suffix = get_random_string(length=6)
            username = f"{primeiro_nome}{unique_suffix}"

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.first_name = nome 
        user.save()

        login(request, user)
        return redirect('teste')

    return render(request, 'core/cadastro.html')


def loginvd(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        
        if user is not None:
            
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user) 
                
                if user.is_staff:
                    return redirect('logado2')  
                else:
                    return redirect('logado')  
            else:
                
                return redirect('loginerro')  

        else:
            
            return redirect('loginerro')  

    return render(request, 'login.html')


from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required  
def adicionar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            especialidade = request.POST.get('especialidade')  
            data_consulta = request.POST.get('data_consulta')
            hora_desejada = request.POST.get('hora_desejada')

            hora_desejada = datetime.strptime(hora_desejada, '%H:%M').time()

            consulta_existente = Paciente.objects.filter(
                especialidade=especialidade,  
                data_consulta=data_consulta,
                hora_desejada=hora_desejada
            ).exists()

            if consulta_existente:
                messages.error(request, "Já existe uma consulta agendada para essa especialidade nesta data e hora.")
                return render(request, 'agendamento_form.html', {'form': form})

            consulta_proxima = Paciente.objects.filter(
                especialidade=especialidade,
                data_consulta=data_consulta
            ).exclude(hora_desejada=hora_desejada)

            for consulta in consulta_proxima:
                hora_consulta_banco = consulta.hora_desejada
                if abs(datetime.combine(datetime.today(), hora_consulta_banco) - datetime.combine(datetime.today(), hora_desejada)) < timedelta(minutes=30):
                    messages.error(request, "O horário escolhido deve ser pelo menos 30 minutos depois do horário já agendado.")
                    return render(request, 'agendamento_form.html', {'form': form})

            
            paciente = form.save(commit=False)
            paciente.especialidade = especialidade
            paciente.save()

           
            user_email = request.user.email  
            if user_email:
                email_subject = "Confirmação de Agendamento"
                email_body = (
                    f"Olá {request.user.first_name},\n\n"
                    f"Seu agendamento foi confirmado!\n"
                    f"Especialidade: {especialidade}\n"
                    f"Data: {data_consulta}\n"
                    f"Horário: {hora_desejada.strftime('%H:%M')}\n\n"
                    "Obrigado por escolher nossos serviços."
                )

                try:
                    send_mail(
                        email_subject,
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [user_email],  
                        fail_silently=False,
                    )
                    messages.success(request, "Consulta Agendada com sucesso e notificação enviada por e-mail.")
                except Exception as e:
                    messages.error(request, "Consulta Agendada, mas houve um erro ao enviar o e-mail.")
            else:
                messages.error(request, "E-mail do usuário logado não encontrado.")

            return redirect('logado')

    else:
        form = PacienteForm()

    return render(request, 'agendamento_form.html', {'form': form})

def get_especialistas(request, especialidade):
    grupo_mapeamento = {
        'nutricionista_geral': 'Nutricionista Geral',
        'nutricionista_infantil': 'Nutricionista Infantil',
        'introducao_alimentar': 'Introdução Alimentar',
        'fisioterapia_geral': 'Fisioterapia Geral',
        'fisioterapia_infantil': 'Fisioterapia Infantil',
    }

    grupo_nome = grupo_mapeamento.get(especialidade)

    if grupo_nome:
        try:
            grupo = Group.objects.get(name=grupo_nome)
            especialistas = User.objects.filter(groups=grupo).values('id', 'username')
            return JsonResponse(list(especialistas), safe=False)
        except Group.DoesNotExist:
            return JsonResponse([], safe=False)
    else:
        return JsonResponse([], safe=False)


def deletar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.delete()
    return redirect('logado2')


def ver_consultas(request):
    especialidade = request.GET.get('especialidade')

    if especialidade:
        if especialidade == "Nutrição Geral":
            return render(request, 'nutricao_geral.html')
        elif especialidade == "Nutrição Infantil":
            return render(request, 'nutricao_infantil.html')
        elif especialidade == "Fisioterapia Geral":
            return render(request, 'fisioterapia_geral.html')
        elif especialidade == "Fisioterapia Infantil":
            return render(request, 'fisioterapia_infantil.html')
        elif especialidade == "Introdução Alimentar":
            return render(request, 'introducao_alimentar.html')
        else:
            return render(request, 'home_logadoM.html')  
    else:
        return render(request, 'home_logadoM.html')


def nutricionistageral(request):
    pacientes = NutricionistaGeral.objects.all()

    for paciente in pacientes:
        paciente.hora_desejada_formatada = paciente.paciente.hora_desejada.strftime('%H:%M')

    return render(request, 'nutricao_geral.html', {'pacientes': pacientes})


def nutricionistainfantil(request):
    pacientes = NutricionistaInfantil.objects.all()
    
    for paciente in pacientes:
        paciente.hora_desejada_formatada = paciente.paciente.hora_desejada.strftime('%H:%M')
        
    return render(request, 'nutricao_infantil.html', {'pacientes': pacientes})


def introducaoalimentar(request):
    pacientes = IntroducaoAlimentar.objects.all()
    
    for paciente in pacientes:
        paciente.hora_desejada_formatada = paciente.paciente.hora_desejada.strftime('%H:%M')
    return render(request, 'introducao_alimentar.html', {'pacientes': pacientes})


def fisioterapiaGeral(request):
    pacientes = FisioterapiaGeral.objects.all()
    
    for paciente in pacientes:
        paciente.hora_desejada_formatada = paciente.paciente.hora_desejada.strftime('%H:%M')
    return render(request, 'fisioterapia_geral.html', {'pacientes': pacientes})


def fisioterapiainfantil(request):
    pacientes = FisioterapiaInfantil.objects.all()
    
    for paciente in pacientes:
        paciente.hora_desejada_formatada = paciente.paciente.hora_desejada.strftime('%H:%M')
    return render(request, 'fisioterapia_infantil.html', {'pacientes': pacientes})




def alterar_senha(request):
    if not request.user.is_authenticated:
        return redirect('carregamento5')  

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current_password):
            
            return redirect('loginERRO')

        if new_password != confirm_password:

            return redirect('loginERRO')

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        
        if user.is_staff:
            return redirect('logado2')
        else:
            return redirect('logado')
    
    return render(request, 'login.html')
    
def lista_consultas(request):
    pacientes = Paciente.objects.all() 
    return render(request, 'home_logado.html', {'pacientes': pacientes})


import random
import string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

def generate_random_password(length=8):

    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
import random
import string


def generate_random_password(length=8):
    
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            try:
                user = User.objects.get(email=email)
                new_password = generate_random_password()
                user.set_password(new_password)
                user.save()

                email_subject = 'Nova Senha'
                email_body = f'Olá {user.first_name},\n\nSua nova senha é: {new_password}\n\nPor favor, use essa senha para acessar sua conta.'
                
                send_mail(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )

                message = {'text': 'Sua nova senha foi enviada para seu e-mail.', 'type': 'success'}

            except User.DoesNotExist:
                message = {'text': 'Nenhum usuário encontrado com este e-mail!', 'type': 'error'}

            except Exception as e:
                message = {'text': 'Erro ao enviar o e-mail! Tente novamente.', 'type': 'error'}

        else:
            message = {'text': 'Nenhum e-mail foi fornecido.', 'type': 'error'}

        return render(request, 'login.html', {'message': message})

    return render(request, 'core/login.html')




