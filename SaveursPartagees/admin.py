from django.contrib import admin
from .models import Utilisateur, Profile, Categorie, Recette, Ingredient, DetailsRecette, Favori, Commentaire, Listedecourses, Notification


admin.site.register(Utilisateur)
admin.site.register(Profile)
admin.site.register(Recette)
admin.site.register(Ingredient)
admin.site.register(Categorie)
admin.site.register(DetailsRecette)
admin.site.register(Favori)
admin.site.register(Commentaire)
admin.site.register(Listedecourses)
admin.site.register(Notification)


