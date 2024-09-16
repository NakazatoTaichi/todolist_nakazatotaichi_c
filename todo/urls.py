from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView, home
from django.views.generic import DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.shortcuts import redirect



app_name = 'todo'

urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='todo:login'), name='logout'),
    path('home/', home, name='home'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/edit/<int:pk>', views.task_edit, name='task_edit'),
    path('task/delete/<int:pk>', DeleteView.as_view(model=Task, success_url=reverse_lazy('todo:home')), name='task_delete'),
    path('task/update_status/', views.update_task_status, name='task_update_status'),
    path('task/restoration_status/<int:pk>', views.restoration_task_status, name='task_restoration_status'),
]