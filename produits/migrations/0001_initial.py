# Generated by Django 5.0.4 on 2024-08-18 22:10

import django.db.models.deletion
import shortuuid.django_fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz0123456789', editable=False, length=5, max_length=5, prefix='', unique=True)),
                ('nom_produit', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image_presentation', models.ImageField(upload_to='')),
                ('gratuit', models.BooleanField(default=False)),
                ('prix_produit', models.FloatField()),
                ('promotion', models.BooleanField(default=False)),
                ('prix_produit_promotion', models.FloatField(null=True)),
                ('duree_promotion', models.DateTimeField(null=True)),
                ('langue_produit', models.CharField(max_length=25)),
                ('categorie_produit', models.CharField(max_length=150)),
                ('taille_Fichier', models.FloatField(default=0, null=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('supprime', models.BooleanField(default=False)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('entreprise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentification.entreprise')),
            ],
            options={
                'verbose_name': 'Produit',
                'verbose_name_plural': 'Produits',
            },
        ),
        migrations.CreateModel(
            name='Acce',
            fields=[
                ('produit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='produits.produit')),
                ('lien', models.URLField(max_length=500)),
            ],
            options={
                'verbose_name': 'Acce',
                'verbose_name_plural': 'Acces',
            },
            bases=('produits.produit',),
        ),
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('produit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='produits.produit')),
                ('nombre_page', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Livre',
                'verbose_name_plural': 'Livres',
            },
            bases=('produits.produit',),
        ),
        migrations.CreateModel(
            name='ProduitNumerique',
            fields=[
                ('produit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='produits.produit')),
                ('type', models.CharField(max_length=50, verbose_name='Pour specifier le type de document')),
            ],
            options={
                'verbose_name': 'Produit Numerique',
                'verbose_name_plural': 'Produit Numeriques',
            },
            bases=('produits.produit',),
        ),
        migrations.CreateModel(
            name='CHECKOUT',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference', models.CharField(max_length=100, null=True)),
                ('slug', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz0123456789', editable=False, length=10, max_length=10, prefix='', unique=True)),
                ('nom_client', models.CharField(max_length=100)),
                ('devise_client', models.CharField(max_length=5)),
                ('status', models.CharField(default='initialiser', max_length=20)),
                ('type', models.CharField(default='Achat', max_length=10)),
                ('pays_client', models.CharField(max_length=50)),
                ('moyen_de_paiement', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=30, null=True)),
                ('email', models.CharField(max_length=30, null=True)),
                ('codeOtp', models.CharField(max_length=10, null=True)),
                ('orderId', models.CharField(default='open_market', max_length=10, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentification.entreprise')),
                ('produit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='produits.produit')),
            ],
        ),
        migrations.CreateModel(
            name='Fichier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fichier', models.FileField(upload_to='')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.produit')),
            ],
        ),
    ]