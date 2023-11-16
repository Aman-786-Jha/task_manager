# tasks/forms.py
import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']

    widgets = {
        'due_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
    }

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < datetime.date.today():
            raise forms.ValidationError("Due date must be in the future.")
        return due_date

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email
