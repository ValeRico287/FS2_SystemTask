from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'¡Bienvenido {user.name}! Tu cuenta ha sido creada exitosamente.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Cuenta'
        return context


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'¡Bienvenido de nuevo, {form.get_user().name}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Correo o contraseña incorrectos.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Has cerrado sesión exitosamente.')
        return super().dispatch(request, *args, **kwargs)
