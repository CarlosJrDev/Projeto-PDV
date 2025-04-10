# Generated by Django 5.1.2 on 2025-04-03 22:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pedidos', '0005_alter_pedido_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pagamento', models.CharField(choices=[('dinheiro', 'Dinheiro'), ('cartao_credito', 'Cartão de Crédito'), ('cartao_debito', 'Cartão de Débito'), ('pix', 'PIX')], max_length=50)),
                ('pago', models.BooleanField(default=False)),
                ('data_pagamento', models.DateTimeField(blank=True, null=True)),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pagamento', to='pedidos.pedido')),
            ],
        ),
    ]
