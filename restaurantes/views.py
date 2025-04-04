from django.shortcuts import render
from .models import Produto

def cardapio(request, mesa_id):
    produtos = Produto.objects.all()
    return render(request, "restaurantes/cardapio.html", {"produtos": produtos, "mesa_id": mesa_id})
