# Generated by Django 5.1.2 on 2025-04-03 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantes', '0004_produto_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesa',
            name='numero',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
