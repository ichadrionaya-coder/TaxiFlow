from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('recherche/', views.recherche, name='recherche'),
    path('ajouter/', views.ajouter_taxi, name='ajouter_taxi'),
    path('taxi/<int:taxi_id>/statut/', views.changer_statut, name='changer_statut'),
]