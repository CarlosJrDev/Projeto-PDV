from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido
from django.utils.html import escape
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

@receiver(post_save, sender=Pedido)
def enviar_pedido_para_cozinha(sender, instance, created, **kwargs):
    if instance.status in ["AG", "EP", "PE"]:  # Só envia se o status for relevante pra cozinha
        channel_layer = get_channel_layer()

        pedido_data = {
            "id": instance.id,
            "mesa": instance.mesa.numero,
            "status": instance.status,
            "status_display": instance.get_status_display(),
            "itens": [
                {
                    "produto": item.produto.nome,
                    "quantidade": item.quantidade
                }
                for item in instance.itens.all()
            ]
        }

        async_to_sync(channel_layer.group_send)(
            "painel_cozinha",
            {
                "type": "receber_pedido",
                "pedido": pedido_data
            }
        )
        async_to_sync(channel_layer.group_send)(
            "painel_caixa",
            {
                "type": "receber_pedido",
                "pedido": pedido_data
            }
        )
