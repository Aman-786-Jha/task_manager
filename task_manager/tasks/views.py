# tasks/views.py
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Task
from .forms import TaskForm, CustomUserCreationForm

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('task_list')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('task_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission. Please check the provided data.')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('task_list')

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Signup successful.')
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid form submission. Please check the provided data.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tasks/user_signup.html', {'form': form})
