from django.shortcuts import render, redirect
from .models import *
from .forms import TaskForm

def home(request):
    tasks = Task.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'hello/index.html',
                  {'tasks':tasks,
                  'form':form})
