# Generated by Django 5.1.1 on 2024-09-27 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0004_itemcarrinho_capa_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemcarrinho',
            name='capa_url',
        ),
    ]
