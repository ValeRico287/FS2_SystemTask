from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Decorador que requiere que el usuario sea Admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión.')
            return redirect('login')
        
        if request.user.role != 'admin':
            messages.error(request, 'No tiene permisos de administrador.')
            raise PermissionDenied
        
        return view_func(request, *args, **kwargs)
    return wrapper


def team_lead_required(view_func):
    """Decorador que requiere que el usuario sea Team Lead o Admin"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión.')
            return redirect('login')
        
        if request.user.role not in ['team_lead', 'admin']:
            messages.error(request, 'No tiene permisos de líder de equipo.')
            raise PermissionDenied
        
        return view_func(request, *args, **kwargs)
    return wrapper


def user_required(view_func):
    """Decorador que requiere que el usuario esté autenticado"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión.')
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def is_team_lead_of(user, team):
    """Verifica si el usuario es el líder del equipo"""
    return team.team_lead == user or user.role == 'admin'


def is_member_of(user, team):
    """Verifica si el usuario es miembro del equipo"""
    return team.members.filter(id=user.id).exists() or is_team_lead_of(user, team)
