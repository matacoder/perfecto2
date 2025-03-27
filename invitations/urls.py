from django.urls import path
from . import views

urlpatterns = [
    path('company/<int:company_id>/invite/', views.create_company_invitation, name='create_company_invitation'),
    path('team/<int:team_id>/invite/', views.create_team_invitation, name='create_team_invitation'),
    path('accept/<uuid:uuid>/', views.invitation_accept, name='invitation_accept'),
    path('my-invitations/', views.invitation_list, name='invitation_list'),
]
