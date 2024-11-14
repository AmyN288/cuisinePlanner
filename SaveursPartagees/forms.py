from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Pour le modèle utilisateur par défaut de Django
from SaveursPartagees.models import Utilisateur  # Importez le modèle Utilisateur depuis votre propre application

from .models import Recette, Ingredient, Notification
from django.contrib.auth.forms import UserCreationForm



class InscriptionForm(UserCreationForm):
    prenom = forms.CharField(max_length=30, required=True, help_text='Entrez votre prénom')
    nom = forms.CharField(max_length=30, required=True, help_text='Entrez votre nom de famille')
    email = forms.EmailField(required=True, help_text='Entrez une adresse e-mail valide')

    class Meta:
        model = Utilisateur
        fields = ['username', 'prenom', 'nom', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.prenom = self.cleaned_data['prenom']
        user.nom = self.cleaned_data['nom']
        if commit:
            user.save()
        return user



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = '__all__'

class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        # Inclure tous les champs du modèle
        fields = '__all__'

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['sujet', 'message']
        widgets = {
            'sujet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet de la notification'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu de la notification'}),
        }