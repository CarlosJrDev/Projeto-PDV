# Generated by Django 5.1.2 on 2025-04-03 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0005_alter_pedido_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('AG', 'Aguardando preparo'), ('EP', 'Em preparo'), ('PE', 'Pronto para entrega'), ('FI', 'Finalizado'), ('PA', 'Pago')], default='AG', max_length=2),
        ),
    ]
