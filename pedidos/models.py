from django.db import models
from restaurantes.models import Mesa
from django.utils.translation import gettext_lazy as _





class ClienteMesa(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)


class Pedido(models.Model):
    class Status(models.TextChoices):
        AGUARDANDO = "AG", _("Aguardando preparo")
        EM_PREPARO = "EP", _("Em preparo")
        PRONTO = "PE", _("Pronto para entrega")
        FINALIZADO = "FI", _("Finalizado")
        PAGO = "PA", _("Pago")
    
    mesa = models.ForeignKey("restaurantes.Mesa", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.AGUARDANDO   
    )
    cliente = models.ForeignKey(ClienteMesa, on_delete=models.SET_NULL, null=True, blank=True)  # <-- aqui
    criado_em = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())
    
    total.short_description = "Total do Pedido"

    

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.numero} ({self.get_status_display()})"
    
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey("restaurantes.Produto", on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} - Pedido {self.pedido.id}"
    

    def subtotal(self):
        return self.quantidade * self.produto.preco  # Pegamos o preço direto do Produto
    



class Carrinho(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def __str__(self):
        return f"Carrinho - Mesa {self.mesa.numero}"


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey('Carrinho', related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey('restaurantes.Produto', on_delete=models.CASCADE)  # ajuste aqui
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantidade * self.produto.preco

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
    



