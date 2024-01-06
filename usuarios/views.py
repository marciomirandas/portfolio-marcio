from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.mail.message import EmailMessage
import os


def registrar(request):
    context = {}
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        tipo = request.POST.get('tipo')
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        senha2 = request.POST.get('senha2')

        context = {
            'nome': nome, 'sobrenome': sobrenome, 'email': email, 'tipo': tipo, 'usuario': usuario
        }

        usuario_banco = User.objects.filter(username=usuario).first()

        if usuario_banco:
            messages.error(request, 'Usuário já existe')
        else:
            if senha == senha2:
                User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome,
                                         last_name=sobrenome, tipo=tipo)
                messages.success(request, 'Usuário criado com sucesso!')
                return redirect(reverse('login'))
            else:
                messages.error(request, 'As senhas são diferentes')
            
    return render(request, 'usuarios/registrar.html', context)


def login(request):
    
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        if usuario and senha:

            usuario_autenticado = authenticate(username=usuario, password=senha)
            
            if usuario_autenticado is not None:
                auth_login(request, usuario_autenticado)
                
                next_url = request.GET.get('next', '')
                
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(reverse('index'))
            else:
                messages.error(request, 'Dados incorretos')
        else:
            messages.error(request, 'Todos os campos são obrigatórios')

    return render(request, 'usuarios/login.html')
    

def logout(request):
    auth_logout(request)
    return redirect(reverse('index'))


def senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        usuario = User.objects.filter(email=email).first()

        if usuario:
            conteudo = f'Você solicitou a recuperação de senha\n\n'

            mail = EmailMessage(
                subject = 'E-mail enviado pelo sistema django',
                body = conteudo,
                from_email = os.environ['FROM_EMAIL'],
                to = [usuario.email,],
                headers = {'Reply-To': os.environ['FROM_EMAIL']}
            )
            mail.send()
            messages.success(request, 'Foi enviado um email com sua senha!')
            return redirect(reverse('login'))

        else:
            messages.error(request, 'Email não cadastrado no sistema')
    
    return render(request, 'usuarios/senha.html')