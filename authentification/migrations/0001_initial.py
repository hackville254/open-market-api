# Generated by Django 5.0.4 on 2024-06-10 16:19

import django.db.models.deletion
import shortuuid.django_fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nom_entreprise', models.CharField(max_length=150)),
                ('devise', models.CharField(default='XAF', max_length=10)),
                ('slug', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvwxyz0123456789', editable=False, length=5, max_length=5, prefix='', unique=True)),
                ('description', models.TextField(verbose_name="Description de l'entreprise")),
                ('logo', models.ImageField(upload_to='logo_entreprise')),
                ('pays', models.CharField(max_length=50)),
                ('ville', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('secteur_activiter', models.CharField(max_length=150)),
                ('is_activate', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=False)),
                ('supprime', models.BooleanField(default=False)),
                ('stokage', models.FloatField(default=50)),
                ('espace_disponible', models.FloatField(default=50)),
                ('date_modification', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Entreprise',
                'verbose_name_plural': 'Entreprises',
            },
        ),
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_de_licence', models.CharField(max_length=15)),
                ('date', models.DateTimeField(auto_now=True)),
                ('e', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentification.entreprise')),
            ],
            options={
                'verbose_name': "Licence d'utilisation",
                'verbose_name_plural': "Licences d'utilisations",
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]