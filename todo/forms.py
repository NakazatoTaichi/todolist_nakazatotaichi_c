from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import CustomUser
from .models import Task
import pytz
from datetime import datetime
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        required=True,
        input_formats=['%Y-%m-%d %H:%M'],
        label="期限",
        initial=datetime.now(pytz.timezone('Asia/Tokyo')),
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'step': 300
        }),
        disabled=False
    )
    class Meta:
        model = Task
        fields = (
            "title",
            "due_date",
            "memo"
        )

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        if due_date and due_date > now:
            return due_date
        raise ValidationError("期限は現在より未来でなければなりません。")

class TaskStatusForm(forms.Form):
    task_id = forms.IntegerField(widget=forms.HiddenInput())