# Generated by Django 5.1.2 on 2025-04-03 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_carrinho_itemcarrinho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('AG', 'Aguardando preparo'), ('EP', 'Em preparo'), ('AP', 'Pronto para entrega'), ('FI', 'Finalizado'), ('PA', 'Pago')], default='AG', max_length=2),
        ),
    ]
