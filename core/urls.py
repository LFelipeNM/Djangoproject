
from django.urls import path  
from .views import *  
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', home, name='home'),
    path('home', home, name='home2'),
    path('login/123', login_page, name='teste'),
    path('carregamento/', carregamento, name='carregamento'),
    path('carregamento/2', carregamento2, name='carregamento2'),
    path('carregamento/3', carregamento3, name='carregamento3'),
    path('carregamento/4', carregamento4, name='carregamento4'),
    path('carregamento/5', carregamento5, name='carregamento5'),
    path('cadastro/123', cadastro, name='cadastro'),  
    path('cadastro/', register, name='cadastro3'),
    path('login/456', loginvd, name='loginvd'),
    path('logado', home_logado, name='logado'),
    path('logado2', home_logadoM, name='logado2'),
    path('agendar', agendamento, name='agendamento'),
    path('agendando/{id}', adicionar_paciente,name='agendou12'),
    path('especialistas/<str:especialidade>/', get_especialistas, name='get_especialistas'),
    path('erro/login',loginerro, name='loginerro'),
    path('erro/cadastro/email',cpfjaexiste, name='emailjaexiste'),
    path('erro/cadastro/senha',senhasdiferentes, name='senhaerradas'),
    path('consultas/nutrigeral', nutricionistageral, name='ntgrl'),
    path('consultas/nutriinfan', nutricionistainfantil, name='ntifn'),
    path('consultas/fisiogeral', fisioterapiaGeral, name='fisiog'),
    path('consultas/fisioinfantil', fisioterapiainfantil, name='fisioinfantil'),
    path('consultas/introducaoalime', introducaoalimentar, name='introducaoa'),
    path('deletar/<int:paciente_id>/', deletar_paciente, name='deletar_paciente'),
    path('consultas/medico', ver_consultas, name='verconsultas'),
    path('alterar-senha/', alterar_senha, name='alterar_senha'),
    path('consultas/homelogado12', lista_consultas, name='lista_consultas'),
    path('reset-password/', reset_password, name='reset_password')

   



   

]
