from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enseignant, Etudiant, Cours, Seance, Presence, CahierTexte
from .forms import CoursForm, EtudiantForm, SeanceForm, PresenceForm, CahierTexteForm, AjouterEtudiantsCoursForm

@login_required
def dashboard(request):
    try:
        enseignant = request.user.enseignant
        cours = Cours.objects.filter(enseignant=enseignant)
        return render(request, 'gestion/dashboard.html', {'cours': cours})
    except Enseignant.DoesNotExist:
        messages.error(request, 'Vous devez être un enseignant pour accéder à cette page.')
        return redirect('login')

@login_required
def liste_cours(request):
    try:
        enseignant = request.user.enseignant
        cours = Cours.objects.filter(enseignant=enseignant)
        return render(request, 'gestion/liste_cours.html', {'cours': cours})
    except Enseignant.DoesNotExist:
        messages.error(request, 'Vous devez être un enseignant pour accéder à cette page.')
        return redirect('login')

@login_required
def creer_cours(request):
    try:
        enseignant = request.user.enseignant
        if request.method == 'POST':
            form = CoursForm(request.POST)
            if form.is_valid():
                cours = form.save(commit=False)
                cours.enseignant = enseignant
                cours.save()
                form.save_m2m()  # Save many-to-many relationships
                messages.success(request, 'Cours créé avec succès.')
                return redirect('liste_cours')
        else:
            form = CoursForm()
        return render(request, 'gestion/creer_cours.html', {'form': form})
    except Enseignant.DoesNotExist:
        messages.error(request, 'Vous devez être un enseignant pour accéder à cette page.')
        return redirect('login')

@login_required
def liste_etudiants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'gestion/liste_etudiants.html', {'etudiants': etudiants})

@login_required
def ajouter_etudiant(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Étudiant ajouté avec succès.')
            return redirect('liste_etudiants')
    else:
        form = EtudiantForm()
    return render(request, 'gestion/ajouter_etudiant.html', {'form': form})

@login_required
def detail_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id, enseignant=request.user.enseignant)
    seances = Seance.objects.filter(cours=cours)
    cahiers = CahierTexte.objects.filter(cours=cours)
    return render(request, 'gestion/detail_cours.html', {'cours': cours, 'seances': seances, 'cahiers': cahiers})

@login_required
def creer_seance(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id, enseignant=request.user.enseignant)
    if request.method == 'POST':
        form = SeanceForm(request.POST)
        if form.is_valid():
            seance = form.save(commit=False)
            seance.cours = cours
            seance.save()
            messages.success(request, 'Séance créée avec succès.')
            return redirect('detail_cours', cours_id=cours.id)
    else:
        form = SeanceForm()
    return render(request, 'gestion/creer_seance.html', {'form': form, 'cours': cours})

@login_required
def faire_appel(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id, cours__enseignant=request.user.enseignant)
    etudiants = seance.cours.etudiants.all()
    if request.method == 'POST':
        for etudiant in etudiants:
            present = request.POST.get(f'present_{etudiant.id}') == 'on'
            Presence.objects.update_or_create(
                seance=seance,
                etudiant=etudiant,
                defaults={'present': present}
            )
        messages.success(request, 'Appel enregistré avec succès.')
        return redirect('detail_cours', cours_id=seance.cours.id)
    presences = Presence.objects.filter(seance=seance)
    presence_dict = {p.etudiant.id: p.present for p in presences}
    etudiant_list = []
    for etudiant in etudiants:
        is_present = presence_dict.get(etudiant.id, False)
        etudiant_list.append({'etudiant': etudiant, 'is_present': is_present})
    return render(request, 'gestion/faire_appel.html', {'seance': seance, 'etudiant_list': etudiant_list})

@login_required
def ajouter_cahier(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id, enseignant=request.user.enseignant)
    if request.method == 'POST':
        form = CahierTexteForm(request.POST)
        if form.is_valid():
            cahier = form.save(commit=False)
            cahier.cours = cours
            cahier.save()
            messages.success(request, 'Cahier de texte ajouté avec succès.')
            return redirect('detail_cours', cours_id=cours.id)
    else:
        form = CahierTexteForm()
    return render(request, 'gestion/ajouter_cahier.html', {'form': form, 'cours': cours})

@login_required
def supprimer_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id, enseignant=request.user.enseignant)
    cours.delete()
    messages.success(request, 'Cours supprimé avec succès.')
    return redirect('liste_cours')

@login_required
def supprimer_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    etudiant.delete()
    messages.success(request, 'Étudiant supprimé avec succès.')
    return redirect('liste_etudiants')

@login_required
def ajouter_etudiants_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id, enseignant=request.user.enseignant)
    if request.method == 'POST':
        form = AjouterEtudiantsCoursForm(request.POST)
        if form.is_valid():
            etudiants_selectionnes = form.cleaned_data['etudiants']
            for etudiant in etudiants_selectionnes:
                cours.etudiants.add(etudiant)
            messages.success(request, f'{etudiants_selectionnes.count()} étudiant(s) ajouté(s) au cours.')
            return redirect('detail_cours', cours_id=cours.id)
    else:
        form = AjouterEtudiantsCoursForm()
    return render(request, 'gestion/ajouter_etudiants_cours.html', {'form': form, 'cours': cours})
