from django import forms
from .models import Cours, Etudiant, Seance, Presence, CahierTexte

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['titre', 'description', 'etudiants']
        widgets = {
            'etudiants': forms.CheckboxSelectMultiple(),
        }

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['matricule', 'nom', 'prenom', 'email', 'date_naissance']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['date', 'description']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['etudiant', 'present']

class CahierTexteForm(forms.ModelForm):
    class Meta:
        model = CahierTexte
        fields = ['titre', 'contenu']

class AjouterEtudiantsCoursForm(forms.Form):
    etudiants = forms.ModelMultipleChoiceField(
        queryset=Etudiant.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Sélectionner les étudiants à ajouter"
    )
