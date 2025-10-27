from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cours/', views.liste_cours, name='liste_cours'),
    path('cours/creer/', views.creer_cours, name='creer_cours'),
    path('cours/<int:cours_id>/', views.detail_cours, name='detail_cours'),
    path('cours/<int:cours_id>/supprimer/', views.supprimer_cours, name='supprimer_cours'),
    path('cours/<int:cours_id>/seance/creer/', views.creer_seance, name='creer_seance'),
    path('seance/<int:seance_id>/appel/', views.faire_appel, name='faire_appel'),
    path('cours/<int:cours_id>/cahier/ajouter/', views.ajouter_cahier, name='ajouter_cahier'),
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/ajouter/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('etudiants/<int:etudiant_id>/supprimer/', views.supprimer_etudiant, name='supprimer_etudiant'),
    path('cours/<int:cours_id>/ajouter-etudiants/', views.ajouter_etudiants_cours, name='ajouter_etudiants_cours'),
]
