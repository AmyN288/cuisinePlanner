# Generated by Django 5.1.3 on 2024-11-10 16:58

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujet', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id_recette', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100, verbose_name='Nom de la recette')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images_recettes/', verbose_name='Image de la recette')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SaveursPartagees.categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Listedecourses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.TextField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recette', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SaveursPartagees.recette')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name="Nom de l'ingrédient")),
                ('quantite', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Quantité de l'ingrédient")),
                ('unite', models.CharField(choices=[('g', 'Gramme'), ('kg', 'Kilogramme'), ('ml', 'Millilitre'), ('l', 'Litre'), ('c.à.s', 'Cuillère à soupe'), ('c.à.c', 'Cuillère à café'), ('pincée', 'Pincée'), ('unité', 'Unité')], default='g', max_length=10, verbose_name='Unité de mesure')),
                ('recette', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='SaveursPartagees.recette', verbose_name='Recette associée')),
            ],
        ),
        migrations.CreateModel(
            name='Favori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recette', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SaveursPartagees.recette')),
            ],
        ),
        migrations.CreateModel(
            name='DetailsRecette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='Description de la recette')),
                ('instructions', models.TextField(blank=True, verbose_name='Instructions de préparation')),
                ('temps_preparation', models.PositiveIntegerField(blank=True, null=True, verbose_name='Temps de préparation (en minutes)')),
                ('temps_cuisson', models.PositiveIntegerField(blank=True, null=True, verbose_name='Temps de cuisson (en minutes)')),
                ('portions', models.PositiveIntegerField(blank=True, null=True, verbose_name='Nombre de portions')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name="URL de l'image")),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('categorie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recettes', to='SaveursPartagees.categorie', verbose_name='Catégorie')),
                ('recette', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='SaveursPartagees.recette', verbose_name='Recette associée')),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.TextField()),
                ('date_commentaire', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recette', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SaveursPartagees.recette')),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('prenom', models.CharField(blank=True, max_length=30, null=True)),
                ('nom', models.CharField(blank=True, max_length=30, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('telephone', models.CharField(blank=True, max_length=15, null=True)),
                ('photo_profil', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('date_inscription', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, related_name='utilisateur_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='utilisateur_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
