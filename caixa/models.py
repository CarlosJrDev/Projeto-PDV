from django.db import models
from pedidos.models import Pedido
from django.utils.timezone import now

class Pagamento(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="pagamento")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_recebido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    troco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    metodo_pagamento = models.CharField(max_length=50, choices=[
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
    ])
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateTimeField(null=True, blank=True)

    def calcular_troco(self):
        """Calcula automaticamente o troco se for pagamento em dinheiro."""
        if self.valor_recebido and self.valor_recebido >= self.valor_total:
            self.troco = self.valor_recebido - self.valor_total
        else:
            self.troco = 0

    def save(self, *args, **kwargs):
        """Atualiza a data de pagamento e calcula o troco antes de salvar."""
        if self.pago and not self.data_pagamento:
            self.data_pagamento = now()
        self.calcular_troco()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pagamento do Pedido {self.pedido.id} - {self.metodo_pagamento}"