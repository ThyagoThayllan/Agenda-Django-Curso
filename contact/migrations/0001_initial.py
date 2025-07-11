# Generated by Django 5.2.2 on 2025-06-24 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('first_name', models.CharField(max_length=50, verbose_name='Nome')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Sobrenome')),
                ('phone', models.CharField(max_length=50, verbose_name='Telefone')),
            ],
        ),
    ]
