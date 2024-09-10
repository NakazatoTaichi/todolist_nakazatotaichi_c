from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from .forms import SignUpForm
from .models import Task
from .forms import TaskForm
from .forms import TaskStatusForm
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

    # 新規作成用フォーム
    task_create_form = TaskForm()

    # 編集用フォーム（初期状態では空）
    task_edit_form = TaskForm()

    context = {
        'today_tasks': today_tasks,
        'completed_tasks': completed_tasks,
        'task_create_form': task_create_form,
        'task_edit_form': task_edit_form,
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
    return redirect('todo:home')

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
    return redirect('todo:home')


def update_task_status(request):
    if request.method == 'POST':
        form = TaskStatusForm(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data['task_id']
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                task.status = 'completed' if 'task_status' in request.POST else 'not_started'
                task.save()
                return redirect('todo:home')
            except Task.DoesNotExist:
                return redirect('todo:home')
    return redirect('todo:home')