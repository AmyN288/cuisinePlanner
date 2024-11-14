from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser



class Utilisateur(AbstractUser):
    # Attributs supplémentaires
    prenom = models.CharField(max_length=30, blank=True, null=True)  # Prénom de l'utilisateur
    nom = models.CharField(max_length=30, blank=True, null=True)     # Nom de famille de l'utilisateur
    date_naissance = models.DateField(blank=True, null=True)  # Date de naissance
    adresse = models.CharField(max_length=255, blank=True, null=True)  # Adresse
    telephone = models.CharField(max_length=15, blank=True, null=True)  # Numéro de téléphone
    photo_profil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Photo de profil
    date_inscription = models.DateTimeField(default=timezone.now)  # Date d'inscription

    # Ajoutez les related_name pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='utilisateur_set',  # Changez ce nom selon vos préférences
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='utilisateur_set',  # Changez ce nom selon vos préférences
        blank=True,
    )

    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom and self.nom else self.username

# Modèle Profile pour étendre les informations d'utilisateur
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Redimensionner l'image si elle est trop grande
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# Modèle Catégorie pour les recettes
class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom
    
# Modèle Recette
class Recette(models.Model):
    id_recette = models.AutoField(primary_key=True) 
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE) 
    nom = models.CharField(max_length=100, verbose_name="Nom de la recette")
    image = models.ImageField(upload_to="images_recettes/", blank=True, null=True, verbose_name="Image de la recette")

    def __str__(self):
        return self.nom
    
    # Le gestionnaire 'objects' est inclus par défaut, pas besoin de le déclarer
    




# Définition des unités de mesure
UNITE_CHOICES = [
    ('g', 'Gramme'),
    ('kg', 'Kilogramme'),
    ('ml', 'Millilitre'),
    ('l', 'Litre'),
    ('c.à.s', 'Cuillère à soupe'),
    ('c.à.c', 'Cuillère à café'),
    ('pincée', 'Pincée'),
    ('unité', 'Unité'),  # Pour les ingrédients qui n'ont pas de poids précis
]

class Ingredient(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de l'ingrédient")
    recette = models.ForeignKey(
        'Recette', on_delete=models.CASCADE, 
        related_name="ingredients", 
        verbose_name="Recette associée"
    )
    quantite = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Quantité de l'ingrédient"
    )
    unite = models.CharField(
        max_length=10, 
        choices=UNITE_CHOICES, 
        default='g', 
        verbose_name="Unité de mesure"
    )

    def __str__(self):
        return f"{self.nom} - {self.quantite} {self.unite}"
    
    


class DetailsRecette(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name="details", verbose_name="Recette associée")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name="recettes", verbose_name="Catégorie")
    description = models.TextField(verbose_name="Description de la recette", blank=True)
    instructions = models.TextField(verbose_name="Instructions de préparation", blank=True)
    temps_preparation = models.PositiveIntegerField(verbose_name="Temps de préparation (en minutes)", blank=True, null=True)
    temps_cuisson = models.PositiveIntegerField(verbose_name="Temps de cuisson (en minutes)", blank=True, null=True)
    portions = models.PositiveIntegerField(verbose_name="Nombre de portions", blank=True, null=True)
    image_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="URL de l'image")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return f"Détails de {self.recette.nom}"


    
    
        
        

# Modèle Favori pour les recettes favorites
class Favori(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.recette.titre}"

# Modèle Commentaire pour les recettes
class Commentaire(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    commentaire = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.recette.titre} - {self.commentaire[:20]}"

# Modèle ListeDeCourse pour gérer les listes de courses liées aux recettes
class Listedecourses(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    items = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Liste de {self.utilisateur.username} pour {self.recette.titre}"

class Notification(models.Model):
    sujet = models.CharField(max_length=255)  # Assurez-vous que ce champ existe
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sujet