from django.forms import CharField, TextInput, PasswordInput, EmailInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    username = CharField(label='Логин:',
                         widget=TextInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте логин'}))
    email = CharField(label='Почта:',
                      widget=EmailInput(attrs={'class': 'form-input', 'placeholder': 'Ваш e-mail'}))
    password1 = CharField(label='Пароль:',
                          widget=PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте пароль'}))
    password2 = CharField(label='Повтор пароля:',
                          widget=PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = CharField(label='Логин:',
                         widget=TextInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте логин'}))
    password = CharField(label='Пароль:',
                         widget=PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Придумайте пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
