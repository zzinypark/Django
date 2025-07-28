from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import all_valid
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from todo.forms import TodoForm, TodoUpdateForm
from todo.models import Todo

@login_required()
def todo_list(request):
    todo_list = Todo.objects.filter(user=request.user).order_by('-created_at')
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )
    paginator = Paginator(todo_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'todo_list.html', context)


@login_required()
def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    context = {
        'todo': todo.__dict__
    }

    return render(request, 'todo_info.html', context)

@login_required()
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect('todo_info', todo_id=todo.id)
    context = {
        'form': form
    }
    return render(request, 'todo_create.html', context)

@login_required()
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid():
        todo.save()
        return redirect('todo_info', todo_id=todo_id)
    context = {
        'form': form
    }
    return render(request, 'todo_update.html', context)

@login_required()
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))