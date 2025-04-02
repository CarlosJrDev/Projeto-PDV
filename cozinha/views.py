from django.shortcuts import render, get_object_or_404, redirect
from pedidos.models import Pedido


def cozinha(request):
    pedidos = Pedido.objects.filter(status__in=["AG", "EP", ]).order_by("criado_em")
    return render(request, "cozinha/cozinha.html", {"pedidos": pedidos})


def atualizar_status(request, pedido_id, novo_status):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = novo_status
    pedido.save()
    return redirect("cozinha")
