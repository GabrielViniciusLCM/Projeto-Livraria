# Generated by Django 5.1.1 on 2024-09-27 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0003_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcarrinho',
            name='capa_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
