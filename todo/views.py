from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.views import View
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required


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
    return render(request, 'todo/home.html')
