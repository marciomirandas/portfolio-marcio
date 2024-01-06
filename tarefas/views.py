from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import *


@login_required
def tarefas(request):
    valor = ''
    if request.method == 'POST':
        pesquisa = request.POST.get('pesquisa')
        opcao = request.POST.get('opcao')
        
        q_pesquisa = Q()
        q_pesquisa &= Q(nome__icontains=pesquisa)
        q_pesquisa &= Q(usuario=request.user)

        if opcao:
            q_pesquisa &= Q(status=opcao)

        todas_tarefas = Tarefa.objects.filter(q_pesquisa).order_by('-id')
        valor = pesquisa
    else:
        todas_tarefas = Tarefa.objects.filter(usuario=request.user).order_by('-id')
        
    paginacao = Paginator(todas_tarefas, 2)
    pagina = request.GET.get('page')
    tarefas = paginacao.get_page(pagina)

    context = {
        'tarefas': tarefas,
        'valor': valor
    }
    return render(request, 'tarefas/tarefas.html', context)


@login_required
def nova_tarefa(request):
    context = {}
    if request.method == 'POST':
        form = TarefaModelForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            tarefa.save()
            messages.success(request, 'Tarefa criada com sucesso!')
            return redirect(reverse('tarefas'))
        else:
            messages.error(request, 'Erro ao criar a tarefa!')
            context['form'] = form
    else:
        form = TarefaModelForm()
        context['form'] = form

    return render(request, 'tarefas/nova_tarefa.html', context)


@login_required
def ver_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)

    if request.user != tarefa.usuario:
        messages.error(request, 'Acesso não permitido!')
        return redirect(reverse('tarefas'))
    
    context = {'tarefa': tarefa}
    return render(request, 'tarefas/ver_tarefa.html', context)


@login_required
def editar_tarefa(request, id):
    context = {}
    tarefa = get_object_or_404(Tarefa, id=id)

    if request.user != tarefa.usuario:
        messages.error(request, 'Acesso não permitido!')
        return redirect(reverse('tarefas'))
    
    if request.method == 'POST':
        form = TarefaModelForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa editada com sucesso!')
            return redirect(reverse('tarefas'))
        else:
            messages.error(request, 'Erro ao editar a tarefa!')
            context['form'] = form
    else:
        form = TarefaModelForm(instance=tarefa)
        context['form'] = form

    return render(request, 'tarefas/editar_tarefa.html', context)


@login_required
def apagar_tarefa(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)

    if request.user != tarefa.usuario:
        messages.error(request, 'Acesso não permitido!')
        return redirect(reverse('tarefas'))
    
    tarefa.delete()
    messages.success(request, 'Tarefa apagada com sucesso!')
    return redirect(reverse('tarefas'))
