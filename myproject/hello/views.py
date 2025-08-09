from re import search

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, EditTaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


@login_required
def home(request):
    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', '')
    tasks = Task.objects.filter(user=request.user)

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    if sort_option == 'date_new':
        tasks = tasks.order_by('-created_at')
    elif sort_option == 'date_old':
        tasks = tasks.order_by('created_at')
    elif sort_option == 'completed':
        tasks = tasks.order_by('-is_completed')
    elif sort_option == 'not_completed':
        tasks = tasks.order_by('is_completed')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'hello/index.html', {'tasks': tasks, 'form': form, 'filter': 'all'})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'hello/register.html', {'form':form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = True
    task.save()
    return redirect('home')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditTaskForm(instance=task)

    return render(request, 'hello/edit.html', {'form': form})

@login_required
def filter_tasks(request, status):
    if status == 'completed':
        tasks = Task.objects.filter(is_completed=True)
    elif status == 'pending':
        tasks = Task.objects.filter(is_completed=False)
    else:
        tasks = Task.objects.all()

    form = TaskForm()
    return render(request, 'hello/index.html', {'tasks': tasks, 'form': form, 'filter': status})