from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Recette, Categorie, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import Notification
from .forms import NotificationForm
from .forms import InscriptionForm

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            connexion(request, user)
            messages.success(request, "Inscription réussie, vous êtes maintenant connecté.")
            return redirect('home')
        else:
            messages.error(request, "Une erreur est survenue lors de l'inscription.")
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

# Vue pour la connexion
def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                connexion(request, user)
                messages.success(request, f"Bienvenue, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()
    return render(request, 'connexion.html', {'form': form})

# Vue pour la déconnexion
def deconnexion(request):
    deconnexion(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('connexion')


@login_required
def envoyer_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            utilisateurs = User.objects.all()  # Envoyer à tous les utilisateurs

            for utilisateur in utilisateurs:
                Notification.objects.create(
                    utilisateur=utilisateur,
                    sujet=sujet,
                    message=message
                )
            messages.success(request, "Notification envoyée à tous les utilisateurs.")
            return redirect('liste_notifications')
    else:
        form = NotificationForm()

    return render(request, 'notifications/envoyer_notification.html', {'form': form})

@login_required
def liste_notifications(request):
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_creation')
    return render(request, 'notifications/liste_notifications.html', {'notifications': notifications})

# Vue pour l'index
@login_required
def index(request):
    recettes = Recette.objects.all()
    context = {
        'recettes': recettes
    }
    return render(request, 'index.html', context)

# Vue pour afficher les catégories
@login_required
def categories(request):
    categories = Categorie.objects.all()
    context = {'categories': categories}
    return render(request, 'categories.html', context)

# Vue pour afficher une recette spécifique
@login_required
def recipe(request):
    recettes = Recette.objects.all()
    context = {'recettes': recipe}
    return render(request, 'recipe.html', context)

# Vue pour la page de contact
@login_required
def contact(request):
    return render(request, 'contact.html')

# Vue principale
@login_required
def main(request):
    return render(request, 'main.html')



# Vue pour ajouter une recette (accès réservé aux utilisateurs connectés)
@login_required
def ajouterRecette(request):
    if request.method == 'POST':
        titre = request.POST['titre']
        description = request.POST['description']
        ingredients = request.POST['ingredients']
        instructions = request.POST['instructions']
        
        nouvelle_recette = Recette.objects.create(
            titre=titre,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            auteur=request.user
        )
        messages.success(request, "Recette ajoutée avec succès.")
        return redirect('recipe')
    
    return render(request, 'ajouterRecette.html')

# Vue pour la liste de courses
@login_required
def liste_de_courses(request):
    # Logique pour générer la liste de courses
    return render(request, 'liste_de_courses.html')

# Vue pour les détails d'une recette
def details_recette(request, id):
    recette = get_object_or_404(Recette, id=id)
    context = {'recette': recette}
    return render(request, 'details_decette.html', context)
