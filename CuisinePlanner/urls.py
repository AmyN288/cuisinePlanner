"""
URL configuration for CuisinePlanner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from SaveursPartagees.views import index,categories,recipe,contact,main,inscription,connexion
from SaveursPartagees.views import deconnexion,ajouterRecette,liste_de_courses,details_recette
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404
from SaveursPartagees.views import envoyer_notification, liste_notifications

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('categories/', categories, name='categories'),
    path('recipe/', recipe, name='recipe'),
    path('contact/', contact, name='contact'),
    path('main/', main, name='main'),
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('ajouterRecette/', ajouterRecette, name='ajouterRecette'),
    path('listedecourses/', liste_de_courses, name='listedecourses'),
     path('details_recette/<int:id>/', details_recette, name='detail_recette'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('envoyer-notification/', envoyer_notification, name='envoyer_notification'),
    path('notifications/', liste_notifications, name='liste_notifications'),
    #path('accounts/login/',connexion, name='login'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



