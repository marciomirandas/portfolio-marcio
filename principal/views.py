from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.core.mail.message import EmailMessage
from django.contrib import messages
import os

def index(request):
    if request.method == 'POST':
        nome = request.POST.get('name')
        email = request.POST.get('email')
        assunto = request.POST.get('subject')
        mensagem = request.POST.get('message')

        if (nome and email and assunto and mensagem):

            conteudo = f'Nome: {nome}\n\nE-mail: {email}\n\nAssunto: {assunto}\n\nMensagem: {mensagem}'

            mail = EmailMessage(
                subject = 'E-mail enviado pelo sistema django',
                body = conteudo,
                from_email = os.environ['FROM_EMAIL'],
                to = [os.environ['TO_EMAIL'],],
                headers = {'Reply-To': email}
            )
            mail.send()

            messages.success(request, 'Email enviado com sucesso!')
        else:
            messages.error(request, 'Erro ao enviar o email!')

        return redirect(reverse('index'))
    else:
        context = {
            'index': True
        }
        return render(request, 'principal/index.html', context)


def error404(request, ex):
    return render(request, 'principal/404.html')


def error500(request):
    return render(request, 'principal/500.html')


def error403(request, exception):
    return render(request, 'principal/403.html')
