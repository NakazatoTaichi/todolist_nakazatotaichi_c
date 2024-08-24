from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from .forms import SignUpForm
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser



class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'todo/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo:home')
        return render(request, 'todo/signup.html', {'form': form})


@login_required
def home(request):
    # 現在の日付と時刻
    now = timezone.now()

    # 現在の日付と時刻に基づいて今日のタスクと完了済みのタスクを取得
    today_tasks = Task.objects.filter(due_date__date=now.date(), status='not_started', user=request.user)
    completed_tasks = Task.objects.filter(status='completed', user=request.user)

    context = {
        'today_tasks': today_tasks,
        'completed_tasks': completed_tasks
    }

    return render(request, 'todo/home.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = CustomUser.objects.get(id=request.user.id)
            task.save()
            return redirect('todo:home')
    else:
        form = TaskForm()
    return render(request, 'todo/task_create.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo:home')
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task
    }
    return render(request, 'todo/task_edit.html', context)