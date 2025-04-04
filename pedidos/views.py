from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrinho, ItemCarrinho, Pedido, ItemPedido
from restaurantes.models import Produto, Mesa

def ver_carrinho(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    carrinho, created = Carrinho.objects.get_or_create(mesa=mesa)
    return render(request, "pedidos/carrinho.html", {"carrinho": carrinho, "mesa": mesa})

def adicionar_ao_carrinho(request, produto_id, mesa_id):
    produto = get_object_or_404(Produto, id=produto_id)
    mesa = get_object_or_404(Mesa, id=mesa_id)
    carrinho, created = Carrinho.objects.get_or_create(mesa=mesa)

    item, item_created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    if not item_created:
        item.quantidade += 1
        item.save()

    return redirect("listar_produtos", mesa_id=mesa.id)  # redireciona pra lista de produtos da mesa

def listar_produtos(request, mesa_id):
    produtos = Produto.objects.all()
    mesa = get_object_or_404(Mesa, id=mesa_id)
    return render(request, "pedidos/lista_produtos.html", {"produtos": produtos, "mesa": mesa})

def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    mesa_id = item.carrinho.mesa.id
    item.delete()
    return redirect("ver_carrinho", mesa_id=mesa_id)

def finalizar_pedido(request, mesa_id):
    carrinho = get_object_or_404(Carrinho, mesa_id=mesa_id)
    
    if carrinho.itens.exists():
        pedido = Pedido.objects.create(mesa=carrinho.mesa)
        for item in carrinho.itens.all():
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade
            )
        carrinho.delete()

    return redirect("cozinha")
