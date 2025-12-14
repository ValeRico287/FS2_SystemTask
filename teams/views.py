from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from accounts.permissions import admin_required, team_lead_required, is_team_lead_of
from accounts.models import User
from .models import Team, TeamMembership


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Team.objects.all()
        elif user.role == 'team_lead':
            return Team.objects.filter(team_lead=user) | Team.objects.filter(members=user)
        else:
            return Team.objects.filter(members=user)


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    template_name = 'teams/team_form.html'
    fields = ['name', 'description', 'team_lead']
    success_url = reverse_lazy('team-list')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, 'Solo los administradores pueden crear equipos.')
            return redirect('team-list')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Solo mostrar usuarios con rol team_lead o admin
        form.fields['team_lead'].queryset = User.objects.filter(role__in=['team_lead', 'admin'])
        return form
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Agregar al team_lead como miembro del equipo
        if self.object.team_lead:
            TeamMembership.objects.get_or_create(
                user=self.object.team_lead,
                team=self.object
            )
        
        messages.success(self.request, f'Equipo "{self.object.name}" creado exitosamente.')
        return response


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        context['members'] = self.object.members.all()
        context['is_team_lead'] = is_team_lead_of(self.request.user, self.object)
        context['is_admin'] = self.request.user.role == 'admin'
        
        # Usuarios disponibles para agregar al equipo
        if context['is_team_lead'] or context['is_admin']:
            context['available_users'] = User.objects.exclude(
                id__in=self.object.members.values_list('id', flat=True)
            ).filter(is_active=True)
        
        return context


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('team-list')
    context_object_name = 'team'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            messages.error(request, 'Solo los administradores pueden eliminar equipos.')
            return redirect('team-list')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        messages.success(request, f'Equipo "{team.name}" eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


@admin_required
def assign_team_lead(request, pk):
    """Vista para que Admin asigne o cambie el líder de un equipo"""
    team = get_object_or_404(Team, pk=pk)
    
    if request.method == 'POST':
        user_id = request.POST.get('team_lead_id')
        if user_id:
            new_lead = get_object_or_404(User, pk=user_id)
            if new_lead.role in ['team_lead', 'admin']:
                team.team_lead = new_lead
                team.save()
                
                # Asegurar que el líder sea miembro del equipo
                TeamMembership.objects.get_or_create(user=new_lead, team=team)
                
                messages.success(request, f'{new_lead.name} es ahora el líder del equipo.')
            else:
                messages.error(request, 'El usuario debe tener rol de Team Lead o Admin.')
        return redirect('team-detail', pk=pk)
    
    team_leads = User.objects.filter(role__in=['team_lead', 'admin'])
    return render(request, 'teams/assign_team_lead.html', {
        'team': team,
        'team_leads': team_leads
    })


@team_lead_required
def add_team_member(request, pk):
    """Vista para que Team Lead agregue miembros al equipo"""
    team = get_object_or_404(Team, pk=pk)
    
    # Verificar que sea el líder del equipo o admin
    if not is_team_lead_of(request.user, team):
        messages.error(request, 'No tienes permisos para agregar miembros a este equipo.')
        return redirect('team-detail', pk=pk)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            membership, created = TeamMembership.objects.get_or_create(
                user=user,
                team=team
            )
            
            if created:
                messages.success(request, f'{user.name} agregado al equipo.')
            else:
                messages.info(request, f'{user.name} ya es miembro del equipo.')
        
        return redirect('team-detail', pk=pk)
    
    # Usuarios que no son miembros del equipo
    available_users = User.objects.exclude(
        id__in=team.members.values_list('id', flat=True)
    ).filter(is_active=True)
    
    # Si es team_lead (no admin), excluir admins de la lista
    if request.user.role == 'team_lead':
        available_users = available_users.exclude(role='admin')
    
    return render(request, 'teams/add_member.html', {
        'team': team,
        'available_users': available_users
    })


@team_lead_required
def remove_team_member(request, pk, user_id):
    """Vista para que Team Lead elimine miembros del equipo"""
    team = get_object_or_404(Team, pk=pk)
    user = get_object_or_404(User, pk=user_id)
    
    # Verificar que sea el líder del equipo o admin
    if not is_team_lead_of(request.user, team):
        messages.error(request, 'No tienes permisos para eliminar miembros de este equipo.')
        return redirect('team-detail', pk=pk)
    
    # No permitir eliminar al líder del equipo
    if team.team_lead == user:
        messages.error(request, 'No puedes eliminar al líder del equipo.')
        return redirect('team-detail', pk=pk)
    
    try:
        membership = TeamMembership.objects.get(team=team, user=user)
        membership.delete()
        messages.success(request, f'{user.name} ha sido eliminado del equipo.')
    except TeamMembership.DoesNotExist:
        messages.error(request, 'El usuario no es miembro del equipo.')
    
    return redirect('team-detail', pk=pk)