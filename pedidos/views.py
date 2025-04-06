from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido, ClienteMesa
from restaurantes.models import Produto, Mesa
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def ver_carrinho(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    carrinho, created = Carrinho.objects.get_or_create(mesa=mesa)
    return render(request, "pedidos/carrinho.html", {"carrinho": carrinho, "mesa": mesa})

def adicionar_ao_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        mesa_id = request.POST.get('mesa_id')

        produto = get_object_or_404(Produto, id=produto_id)
        mesa = get_object_or_404(Mesa, id=mesa_id)

        carrinho, _ = Carrinho.objects.get_or_create(mesa=mesa)
        item, created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)

        if created:
            item.quantidade = 1
        else:
            item.quantidade += 1
        item.save()

        total_itens = carrinho.itens.aggregate(total=Sum('quantidade'))['total'] or 0

        return JsonResponse({'mensagem': 'Produto adicionado!', 'total_itens': total_itens})
    

def listar_produtos(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    produtos = Produto.objects.all()
    carrinho = Carrinho.objects.filter(mesa=mesa).first()

    total_itens = 0
    if carrinho:
        total_itens = carrinho.itens.aggregate(total=Sum('quantidade'))['total'] or 0

    return render(request, 'pedidos/cardapio.html', {
        'mesa': mesa,
        'produtos': produtos,
        'total_itens': total_itens,
    })


def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    mesa_id = item.carrinho.mesa.id
    item.delete()
    return redirect("ver_carrinho", mesa_id=mesa_id)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def finalizar_pedido(request, mesa_id):
    carrinho = get_object_or_404(Carrinho, mesa_id=mesa_id)

    if carrinho.itens.exists():
        cliente = ClienteMesa.objects.filter(mesa_id=mesa_id).last()

        pedido = Pedido.objects.create(
            mesa=carrinho.mesa,
            cliente=cliente,
            status="AG"  # Garante o status inicial
        )

        for item in carrinho.itens.all():
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade
            )

        carrinho.delete()

        # Serializar os dados do pedido
        pedido_data = {
            "id": pedido.id,
            "mesa": pedido.mesa.numero,
            "status": pedido.status,
            "status_display": pedido.get_status_display(),
            "itens": [
                {"quantidade": item.quantidade, "produto": item.produto.nome}
                for item in pedido.itens.all()
            ]
        }

        # Enviar via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "cozinha",
            {
                "type": "novo_pedido",
                "pedido": pedido_data
            }
        )

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Carrinho vazio"})






def quantidade_itens(request, mesa_id):
    carrinho = Carrinho.objects.filter(mesa_id=mesa_id).first()
    quantidade = 0
    if carrinho:
        quantidade = sum(item.quantidade for item in carrinho.itemcarrinho_set.all())
    return JsonResponse({'quantidade': quantidade})



@csrf_exempt
def salvar_dados_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        mesa_id = request.POST.get('mesa_id')

        ClienteMesa.objects.create(nome=nome, telefone=telefone, mesa_id=mesa_id)

        return redirect('listar_produtos', mesa_id=mesa_id)
    

@csrf_exempt
def salvar_cliente_mesa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        mesa_id = request.POST.get('mesa_id')

        # Salve no banco como quiser
        ClienteMesa.objects.create(nome=nome, telefone=telefone, mesa_id=mesa_id)

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'erro'}, status=400)