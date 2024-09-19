from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from .forms import SignUpForm
from .models import Task
from .forms import TaskForm
from .forms import TaskStatusForm
from .forms import GoalForm
from .models import Goal
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.db.models import Q
from django.views.generic.edit import DeleteView
from django.core.exceptions import ValidationError


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'todo/signup.html', {'form': form})

    @csrf_exempt
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'ようこそ！')
            return redirect('todo:home')
        return render(request, 'todo/signup.html', {'form': form})


class LoginView(AuthLoginView):
    template_name = 'todo/login.html'
    @csrf_exempt
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'ログインしました。')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'ログインに失敗しました。名前またはパスワードが間違っています。')
        return super().form_invalid(form)

@login_required
def home(request):
    # 現在の日付と時刻
    now = timezone.now()

    my_goals = Goal.objects.filter(
        user=request.user
    )
    today_tasks = Task.objects.filter(
        due_date__date=now.date(),
        status='not_started',
        user=request.user
    )
    create_tasks = Task.objects.filter(
        ~Q(due_date__date=now.date()),
        status='not_started',
        user=request.user
    )
    completed_tasks = Task.objects.filter(
        status='completed',
        user=request.user
    )

    # 新しいタスク追加のフォーム
    task_create_form = TaskForm()

    context = {
        'my_goals': my_goals,
        'today_tasks': today_tasks,
        'create_tasks': create_tasks,
        'completed_tasks': completed_tasks,
        'task_create_form': task_create_form,
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
            messages.success(request, '新しいタスクを追加しました。')
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
            messages.success(request, 'タスクを編集しました。')
            return redirect('todo:home')
    else:
        form = TaskForm(instance=task)
        context = {
        'form': form,
        'task': task
    }
    return render(request, 'todo/task_edit.html', context)

@login_required
def update_task_status(request):
    if request.method == 'POST':
        form = TaskStatusForm(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data['task_id']
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                task.status = 'completed' if 'task_status' in request.POST else 'not_started'
                task.save()
                messages.success(request, task.title + 'を完了済みにしました。')
                return redirect('todo:home')
            except Task.DoesNotExist:
                messages.error(request, 'タスクが存在しません。')
                return redirect('todo:home')
    return redirect('todo:home')

@login_required
def restoration_task_status(request, pk):
    try:
        task = get_object_or_404(Task, id=pk, user=request.user)
        task.status = 'not_started'  # ステータスを復元（未着手状態にする）
        task.save()
        messages.success(request, task.title + 'を復元しました。')
        return redirect('todo:home')
    except Task.DoesNotExist:
        messages.error(request, 'タスクが存在しません。')
        return redirect('todo:home')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('todo:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'タスクが削除されました。')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'タスクの削除に失敗しました。')
        return super().form_invalid(form)

@login_required
def set_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            if Goal.objects.filter(user=request.user).count() >= 3:
                form.add_error(None, '目標は最大３つまで設定することができます。')
            else:
                goal = form.save(commit=False)
                goal.user = request.user
                goal.save()
                messages.success(request, '目標を設定しました。')
                return redirect('todo:home')
    else:
        form = GoalForm()
    return render(request, 'todo/set_goal.html', {'form': form})

@login_required
def delete_goals(request):
    if request.method == 'POST':
        Goal.objects.filter(user=request.user).delete()
        messages.success(request, '設定した目標を削除しました。')
        return redirect('todo:home')
    else:
        return redirect('todo:home')