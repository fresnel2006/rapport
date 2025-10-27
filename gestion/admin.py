from django.contrib import admin
from .models import Enseignant, Etudiant, Cours, Seance, Presence, CahierTexte

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email')

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'email')

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'enseignant')

@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ('cours', 'date')

@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ('seance', 'etudiant', 'present')

@admin.register(CahierTexte)
class CahierTexteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'date_creation')
