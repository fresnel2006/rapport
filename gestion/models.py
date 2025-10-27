from django.db import models
from django.contrib.auth.models import User

# Modèle Enseignant
class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# Modèle Étudiant
class Etudiant(models.Model):
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_naissance = models.DateField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# Modèle Cours
class Cours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    etudiants = models.ManyToManyField(Etudiant, related_name='cours')

    def __str__(self):
        return self.titre

# Modèle Séance (pour les appels)
class Seance(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cours.titre} - {self.date}"

# Modèle Présence
class Presence(models.Model):
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('seance', 'etudiant')

    def __str__(self):
        return f"{self.etudiant} - {self.seance} - {'Présent' if self.present else 'Absent'}"

# Modèle Cahier de Textes
class CahierTexte(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
