from django.contrib import admin
from .models import Taxi, Chauffeur, Zone

# Personnalisation de l'affichage dans /admin

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['nom_zone', 'tarif_base']
    search_fields = ['nom_zone']


@admin.register(Chauffeur)
class ChauffeurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'numero_permis', 'telephone']
    search_fields = ['nom', 'prenom', 'numero_permis']


@admin.register(Taxi)
class TaxiAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ['plaque', 'chauffeur', 'statut', 'zone', 'date_mise_circulation']
    # Filtres latéraux
    list_filter = ['statut', 'zone', 'disponibilite']
    # Barre de recherche
    search_fields = ['plaque', 'chauffeur__nom']
    # Modification directe du statut depuis la liste
    list_editable = ['statut']