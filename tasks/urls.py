from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('mis-tareas/', views.MyTasksView.as_view(), name='my-tasks'),
    path('task/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<uuid:uuid>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/<uuid:uuid>/edit/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<uuid:uuid>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('task/<uuid:uuid>/update-status/', views.update_task_status, name='update-task-status'),
]