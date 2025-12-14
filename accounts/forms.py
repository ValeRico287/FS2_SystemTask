from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'role', 'password1', 'password2')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'mb-3'
        
        # Personalizar labels y placeholders
        self.fields['name'].label = 'Nombre Completo'
        self.fields['email'].label = 'Correo Electrónico'
        self.fields['role'].label = 'Rol'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password2'].label = 'Confirmar Contraseña'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'
        
        # Remover help texts
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].help_text = None
        
        self.helper.add_input(Submit('submit', 'Registrarse', css_class='btn btn-primary w-100'))


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'correo@ejemplo.com',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'mb-3'
        
        self.helper.add_input(Submit('submit', 'Iniciar Sesión', css_class='btn btn-primary w-100'))