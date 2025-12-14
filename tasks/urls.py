from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('mis-tareas/', views.MyTasksView.as_view(), name='my-tasks'),
    path('task/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<int:pk>/update-status/', views.update_task_status, name='update-task-status'),
]