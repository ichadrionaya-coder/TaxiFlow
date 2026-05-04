from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Taxi, Chauffeur, Zone

# ─── VUE 1 : DASHBOARD ────────────────────────────────────────────────────────
# Page d'accueil du régulateur. Affiche les statistiques globales + liste taxis.
def dashboard(request):
    taxis = Taxi.objects.select_related('chauffeur', 'zone').all()
    
    # Statistiques pour les cartes du haut
    total = taxis.count()
    libres = taxis.filter(statut='libre').count()
    en_course = taxis.filter(statut='en_course').count()
    hors_service = taxis.filter(statut='hors_service').count()
    
    # Taxis nécessitant maintenance (âge > 5 ans)
    maintenance = [t for t in taxis if t.necessite_maintenance]

    context = {
        'taxis': taxis,
        'total': total,
        'libres': libres,
        'en_course': en_course,
        'hors_service': hors_service,
        'maintenance_count': len(maintenance),
    }
    return render(request, 'gestion/dashboard.html', context)


# ─── VUE 2 : CHANGER LE STATUT D'UN TAXI ──────────────────────────────────────
# Permet au régulateur de modifier rapidement le statut (Libre / En course / Hors service)
def changer_statut(request, taxi_id):
    taxi = get_object_or_404(Taxi, id=taxi_id)
    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        if nouveau_statut in ['libre', 'en_course', 'hors_service']:
            taxi.statut = nouveau_statut
            taxi.disponibilite = (nouveau_statut == 'libre')
            taxi.save()
    return redirect('dashboard')


# ─── VUE 3 : RECHERCHE ET FILTRAGE ────────────────────────────────────────────
# Filtre les taxis par plaque, chauffeur, zone ou disponibilité
def recherche(request):
    taxis = Taxi.objects.select_related('chauffeur', 'zone').all()
    zones = Zone.objects.all()

    # Récupérer les paramètres GET du formulaire de recherche
    q = request.GET.get('q', '')           # Recherche texte (plaque ou chauffeur)
    zone_id = request.GET.get('zone', '')  # Filtre par zone
    dispo = request.GET.get('disponibilite', '')  # Filtre disponibilité

    if q:
        taxis = taxis.filter(
            Q(plaque__icontains=q) |
            Q(chauffeur__nom__icontains=q) |
            Q(chauffeur__prenom__icontains=q)
        )
    if zone_id:
        taxis = taxis.filter(zone_id=zone_id)
    if dispo:
        taxis = taxis.filter(disponibilite=(dispo == 'true'))

    context = {
        'taxis': taxis,
        'zones': zones,
        'q': q,
        'zone_id': zone_id,
        'dispo': dispo,
    }
    return render(request, 'gestion/recherche.html', context)


# ─── VUE 4 : AJOUTER UN TAXI ──────────────────────────────────────────────────
def ajouter_taxi(request):
    chauffeurs = Chauffeur.objects.all()
    zones = Zone.objects.all()

    if request.method == 'POST':
        plaque = request.POST.get('plaque')
        chauffeur_id = request.POST.get('chauffeur')
        zone_id = request.POST.get('zone')
        date_circ = request.POST.get('date_mise_circulation')

        taxi = Taxi(
            plaque=plaque,
            date_mise_circulation=date_circ,
        )
        if chauffeur_id:
            taxi.chauffeur_id = chauffeur_id
        if zone_id:
            taxi.zone_id = zone_id
        taxi.save()
        return redirect('dashboard')

    return render(request, 'gestion/ajouter_taxi.html', {
        'chauffeurs': chauffeurs,
        'zones': zones
    })