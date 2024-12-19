from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Paciente



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'especialidade', 'genero', 'data_consulta', 'hora_desejada', 'observacoes']

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Não encontramos um usuário com esse e-mail.")
        return email

