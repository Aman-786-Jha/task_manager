# tasks/urls.py
from django.urls import path
from .views import task_list, task_detail, task_create, task_update, task_delete, user_login, user_logout, user_signup

urlpatterns = [
    path('', task_list, name='task_list'),
    path('task/<int:pk>/', task_detail, name='task_detail'),
    path('task/new/', task_create, name='task_create'),
    path('task/<int:pk>/edit/', task_update, name='task_update'),
    path('task/<int:pk>/delete/', task_delete, name='task_delete'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
]
