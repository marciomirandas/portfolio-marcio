from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rolepermissions.decorators import has_permission_decorator, has_role_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *


def site(request):
    context = {
        'slides' : Materia.objects.filter(slide=True).order_by('-id')[:3],
        'importantes' : Materia.objects.filter(importante=True, slide=False).order_by('-id')[:2],
        'materias' : Materia.objects.filter(importante=False, slide=False).order_by('-id')
    }
    return render(request, 'conteudo/site.html', context)


def materia(request, id):
    materia = get_object_or_404(Materia, id=id)
    context = {
        'materia' : materia
    }
    return render(request, 'conteudo/materia.html', context)
    

@login_required()
@has_permission_decorator('administrativo')
def adm_conteudo(request):
    context = {
        'materias' : Materia.objects.all()
    }
    return render(request, 'conteudo/adm_conteudo.html', context)


@login_required()
@has_permission_decorator('administrativo')
def nova_materia(request):
    context = {}
    if request.method == 'POST':
        form = MateriaModelForm(request.POST, request.FILES)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.usuario = request.user
            materia.save()
            messages.success(request, 'Matéria criada com sucesso!')
            return redirect(reverse('adm-conteudo'))
        else:
            messages.error(request, 'Erro ao criar a matéria!')
            context['form'] = form
    else:
        form = MateriaModelForm()
        context['form'] = form

    return render(request, 'conteudo/nova_materia.html', context)


@login_required()
@has_permission_decorator('administrativo')
def editar_materia(request, id):
    context = {}
    materia = get_object_or_404(Materia, id=id)
    if request.method == 'POST':
        form = MateriaModelForm(request.POST, request.FILES, instance=materia)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.usuario = request.user
            materia.save()
            messages.success(request, 'Matéria editada com sucesso!')
            return redirect(reverse('adm-conteudo'))
        else:
            messages.error(request, 'Erro ao editar a Matéria!')
            context['form'] = form
    else:
        form = MateriaModelForm(instance=materia)
        context['form'] = form

    return render(request, 'conteudo/editar_materia.html', context)


@login_required()
@has_permission_decorator('administrativo')
def apagar_materia(request, id):
    tarefa = get_object_or_404(Materia, id=id)
    tarefa.delete()
    messages.success(request, 'Matéria apagada com sucesso!')
    return redirect(reverse('adm-conteudo'))