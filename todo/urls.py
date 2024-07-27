from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView, home


app_name = 'todo'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='todo:login'), name='logout'),
    path('home/', home, name='home'),
]