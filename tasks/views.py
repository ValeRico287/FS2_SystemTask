from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.db.models import Count, Q
from accounts.permissions import team_lead_required, user_required, is_team_lead_of
from accounts.models import User
from teams.models import Team
from notifications.services import notify_task_created
from .models import Task, Comment


class DashboardView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/dashboard.html'
    context_object_name = 'tasks'
    paginate_by = None
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all().select_related('team', 'created_by').prefetch_related('assigned_to').distinct()
        else:
            return Task.objects.filter(
                Q(assigned_to=user) | Q(team__members=user)
            ).select_related('team', 'created_by').prefetch_related('assigned_to').distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Obtener todas las tareas
        all_tasks = self.get_queryset()
        
        # Separar por estado para el Kanban board
        context['to_do_tasks'] = all_tasks.filter(status='to_do')
        context['in_progress_tasks'] = all_tasks.filter(status='in_progress')
        context['review_tasks'] = all_tasks.filter(status='review')
        context['done_tasks'] = all_tasks.filter(status='done')
        
        # Contadores para las estadísticas
        context['to_do_count'] = context['to_do_tasks'].count()
        context['in_progress_count'] = context['in_progress_tasks'].count()
        context['review_count'] = context['review_tasks'].count()
        context['done_count'] = context['done_tasks'].count()
        
        # Tareas asignadas al usuario actual (mis tareas)
        context['my_tasks'] = all_tasks.filter(assigned_to=user).order_by('-created_at')[:5]
        context['my_tasks_count'] = all_tasks.filter(assigned_to=user).count()
        
        # Equipos del usuario
        if user.role == 'admin':
            context['my_teams'] = Team.objects.all().prefetch_related('members').order_by('name')
        elif user.role == 'team_lead':
            context['my_teams'] = Team.objects.filter(
                Q(team_lead=user) | Q(members=user)
            ).prefetch_related('members').order_by('name')
        else:
            context['my_teams'] = Team.objects.filter(members=user).prefetch_related('members').order_by('name')
        
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'team', 'priority', 'due_date']
    success_url = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in ['team_lead', 'admin']:
            messages.error(request, 'Solo los líderes de equipo y administradores pueden crear tareas.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        # Filtrar equipos según el rol
        if user.role == 'admin':
            form.fields['team'].queryset = Team.objects.all()
        elif user.role == 'team_lead':
            form.fields['team'].queryset = Team.objects.filter(team_lead=user)
        
        return form
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Asignar usuarios a la tarea desde el POST
        assigned_user_ids = self.request.POST.getlist('assigned_to')
        if assigned_user_ids:
            assigned_users = User.objects.filter(id__in=assigned_user_ids)
            self.object.assigned_to.set(assigned_users)
            
            # Enviar notificaciones
            notify_task_created(self.object)
        
        messages.success(self.request, 'Tarea creada exitosamente.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener usuarios disponibles según el equipo
        user = self.request.user
        if user.role == 'admin':
            context['available_users'] = User.objects.filter(is_active=True)
        elif user.role == 'team_lead':
            # Usuarios de los equipos del líder
            team_ids = Team.objects.filter(team_lead=user).values_list('id', flat=True)
            context['available_users'] = User.objects.filter(
                teams__id__in=team_ids
            ).distinct()
        
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['can_edit'] = (
            self.request.user.role in ['admin', 'team_lead'] and
            (self.request.user.role == 'admin' or is_team_lead_of(self.request.user, self.object.team))
        )
        context['can_change_status'] = self.object.assigned_to.filter(id=self.request.user.id).exists()
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'team', 'priority', 'due_date', 'status']
    success_url = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        
        # Solo team leads del equipo o admins pueden editar
        if user.role == 'admin' or (user.role == 'team_lead' and is_team_lead_of(user, task.team)):
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permisos para editar esta tarea.')
            return redirect('task-detail', pk=task.pk)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Actualizar usuarios asignados
        assigned_user_ids = self.request.POST.getlist('assigned_to')
        if assigned_user_ids:
            assigned_users = User.objects.filter(id__in=assigned_user_ids)
            self.object.assigned_to.set(assigned_users)
        
        messages.success(self.request, 'Tarea actualizada exitosamente.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_users'] = self.object.team.members.all()
        context['assigned_users'] = self.object.assigned_to.all()
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        
        # Solo team leads del equipo o admins pueden eliminar
        if user.role == 'admin' or (user.role == 'team_lead' and is_team_lead_of(user, task.team)):
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'No tienes permisos para eliminar esta tarea.')
            return redirect('task-detail', pk=task.pk)


class MyTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/my_tasks.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        return Task.objects.filter(
            assigned_to=self.request.user
        ).select_related('team', 'created_by').prefetch_related('assigned_to').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        all_tasks = self.get_queryset()
        
        context['to_do_tasks'] = all_tasks.filter(status='to_do').count()
        context['in_progress_tasks'] = all_tasks.filter(status='in_progress').count()
        context['review_tasks'] = all_tasks.filter(status='review').count()
        context['done_tasks'] = all_tasks.filter(status='done').count()
        
        return context


@user_required
def update_task_status(request, pk):
    """Vista para que usuarios cambien el estado de sus tareas asignadas"""
    task = get_object_or_404(Task, pk=pk)
    
    # Verificar que el usuario esté asignado a la tarea
    if not task.assigned_to.filter(id=request.user.id).exists():
        messages.error(request, 'No tienes permisos para actualizar esta tarea.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['to_do', 'in_progress', 'review', 'done']:
            task.status = new_status
            task.save()
            messages.success(request, f'Estado de la tarea actualizado a {task.get_status_display()}.')
        else:
            messages.error(request, 'Estado inválido.')
        
        return redirect('task-detail', pk=pk)
    
    return render(request, 'tasks/update_status.html', {
        'task': task,
        'status_choices': Task.STATUS_CHOICES
    })