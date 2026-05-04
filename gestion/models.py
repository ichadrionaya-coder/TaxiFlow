from django.db import models

# ─── MODÈLE ZONE ─────────────────────────────────────────────────────────────
class Zone(models.Model):
    nom_zone = models.CharField(max_length=100, verbose_name="Nom de la zone")
    tarif_base = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Tarif de base (MAD)")

    def __str__(self):
        return self.nom_zone

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"


# ─── MODÈLE CHAUFFEUR ─────────────────────────────────────────────────────────
class Chauffeur(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    numero_permis = models.CharField(max_length=50, unique=True, verbose_name="N° Permis")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Chauffeur"
        verbose_name_plural = "Chauffeurs"


# ─── MODÈLE TAXI ──────────────────────────────────────────────────────────────
class Taxi(models.Model):
    STATUT_CHOICES = [
        ('libre', 'Libre'),
        ('en_course', 'En course'),
        ('hors_service', 'Hors service'),
    ]

    plaque = models.CharField(max_length=20, unique=True, verbose_name="Plaque d'immatriculation")
    chauffeur = models.ForeignKey(
        Chauffeur,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Chauffeur assigné"
    )
    disponibilite = models.BooleanField(default=True, verbose_name="Disponible")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='libre', verbose_name="Statut")
    zone = models.ForeignKey(
        Zone,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Zone d'opération"
    )
    date_mise_circulation = models.DateField(verbose_name="Date de mise en circulation")

    def __str__(self):
        return self.plaque

    @property
    def necessite_maintenance(self):
        from datetime import date
        age = (date.today() - self.date_mise_circulation).days // 365
        return age >= 5

    class Meta:
        verbose_name = "Taxi"
        verbose_name_plural = "Taxis"
        ordering = ['plaque']