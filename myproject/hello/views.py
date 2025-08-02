from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, EditTaskForm

def home(request):
    tasks = Task.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()

    return render(request, 'hello/index.html', {'tasks': tasks, 'form': form, 'filter': 'all'})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = True
    task.save()
    return redirect('home')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')

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

def filter_tasks(request, status):
    if status == 'completed':
        tasks = Task.objects.filter(is_completed=True)
    elif status == 'pending':
        tasks = Task.objects.filter(is_completed=False)
    else:
        tasks = Task.objects.all()

    form = TaskForm()
    return render(request, 'hello/index.html', {'tasks': tasks, 'form': form, 'filter': status})