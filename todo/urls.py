from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView, home
from .views import LoginView
from .views import TaskDeleteView
from .models import Task
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static



app_name = 'todo'

urlpatterns = [
    path('', lambda request: redirect('login/')),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='todo:login'), name='logout'),
    path('home/', home, name='home'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/edit/<int:pk>', views.task_edit, name='task_edit'),
    path('task/delete/<int:pk>', TaskDeleteView.as_view(), name='task_delete'),
    path('task/update_status/', views.update_task_status, name='task_update_status'),
    path('task/restoration_status/<int:pk>', views.restoration_task_status, name='task_restoration_status'),
    path('set_goal/', views.set_goal, name='set_goal'),
    path('delete_goals/', views.delete_goals, name='delete_goals'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)