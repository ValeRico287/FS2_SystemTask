from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeamListView.as_view(), name='team-list'),
    path('new/', views.TeamCreateView.as_view(), name='team-create'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('<int:pk>/delete/', views.TeamDeleteView.as_view(), name='team-delete'),
    path('<int:pk>/assign-lead/', views.assign_team_lead, name='assign-team-lead'),
    path('<int:pk>/add-member/', views.add_team_member, name='add-team-member'),
    path('<int:pk>/remove-member/<int:user_id>/', views.remove_team_member, name='remove-team-member'),
]
