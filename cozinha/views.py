from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from pedidos.models import Pedido
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.decorators.csrf import csrf_exempt


def cozinha(request):
    pedidos = Pedido.objects.filter(status__in=["AG", "EP"]).order_by("criado_em")

    pedidos_por_status = {
        "AG": pedidos.filter(status="AG"),
        "EP": pedidos.filter(status="EP"),
    }

    status_nomes = {
        "AG": "Aguardando preparo",
        "EP": "Em preparo",
    }

    context = {
        "pedidos_por_status": pedidos_por_status,
        "status_nomes": status_nomes,
    }

    return render(request, "cozinha/cozinha.html", context)


@csrf_exempt  # (use apenas para testes; em produção, use o CSRF corretamente)
def atualizar_status(request, pedido_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            novo_status = data.get("status")

            pedido = Pedido.objects.get(id=pedido_id)
            pedido.status = novo_status
            pedido.save()

            # Envia atualização pro grupo do caixa
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "caixa",  # <-- Grupo do caixa
                {
                    "type": "receber_pedido",
                    "content": {
                        "id": pedido.id,
                        "mesa": pedido.mesa.numero,
                        "status": pedido.status,
                        "status_display": pedido.get_status_display(),
                        "itens": [
                            {"produto": item.produto.nome, "quantidade": item.quantidade}
                            for item in pedido.itens.all()
                        ]
                    }
                }
            )

            return JsonResponse({
                "success": True,
                "pedido": {
                    "id": pedido.id,
                    "mesa": pedido.mesa.numero,
                    "status": pedido.status,
                    "status_display": pedido.get_status_display(),
                    "itens": [
                        {"produto": item.produto.nome, "quantidade": item.quantidade}
                        for item in pedido.itens.all()
                    ]
                }
            })
        except Pedido.DoesNotExist:
            return JsonResponse({"success": False, "error": "Pedido não encontrado"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Método inválido"})



def pedidos_json(request):
    pedidos = Pedido.objects.select_related("mesa").prefetch_related("itens__produto").all()

    data = []
    for pedido in pedidos:
        itens = [
            {"quantidade": item.quantidade, "produto": item.produto.nome}
            for item in pedido.itens.all()
        ]
        data.append({
            "id": pedido.id,
            "mesa": pedido.mesa.numero,
            "status": pedido.status,
            "status_display": pedido.get_status_display(),
            "itens": itens,
        })

    return JsonResponse({"pedidos": data})