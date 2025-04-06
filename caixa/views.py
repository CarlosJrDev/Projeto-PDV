from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localtime
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.utils.timezone import now
from decimal import Decimal
from pedidos.models import Pedido
from restaurantes.models import Mesa, Restaurante
from .models import Pagamento

def caixa(request):
    mesas = Mesa.objects.all()
    pedidos = Pedido.objects.all()

    # Criamos um dicionário que associa cada mesa ao pedido (se existir)
    pedidos_por_mesa = {pedido.mesa.id: pedido for pedido in pedidos}

    # Adicionamos `pedido` como um atributo de cada mesa
    for mesa in mesas:
        mesa.pedido = pedidos_por_mesa.get(mesa.id, None)

    return render(request, "caixa/caixa.html", {
        "mesas": mesas
    })




def detalhe_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == "POST":
        metodo_pagamento = request.POST.get("metodo_pagamento")
        valor_recebido_input = request.POST.get("valor_recebido")

        valor_total = pedido.total()

        if metodo_pagamento == "dinheiro":
            valor_recebido = Decimal(valor_recebido_input) if valor_recebido_input else Decimal("0.00")
        else:
            valor_recebido = valor_total

        Pagamento.objects.create(
            pedido=pedido,
            valor_total=valor_total,
            valor_recebido=valor_recebido,
            metodo_pagamento=metodo_pagamento,
            pago=True,
        )
        pedido.status = Pedido.Status.FINALIZADO
        pedido.save()

        return redirect("confirmacao_pagamento", pedido_id=pedido.id)

    return render(request, "caixa/detalhe_pagamento.html", {
        "pedido": pedido,
        "valor_total": pedido.total()
    })






def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "caixa/detalhe_pedido.html", {"pedido": pedido})





def gerar_comprovante(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    pagamento = getattr(pedido, "pagamento", None)

    buffer = BytesIO()

    # Impressora térmica 80mm
    width_mm = 80
    height_mm = 200
    width_pt = width_mm * 2.83
    height_pt = height_mm * 2.83

    p = canvas.Canvas(buffer, pagesize=(width_pt, height_pt))
    y = height_pt - 20

    restaurante = Restaurante.objects.first()
    nome_restaurante = restaurante.nome if restaurante else "Restaurante Padrão"

    buffer = BytesIO()

    width_mm = 80
    height_mm = 200
    width_pt = width_mm * 2.83
    height_pt = height_mm * 2.83

    p = canvas.Canvas(buffer, pagesize=(width_pt, height_pt))
    y = height_pt - 20

    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width_pt / 2, y, nome_restaurante)
    y -= 20

    # Dados do pedido
    p.setFont("Helvetica", 8)
    p.drawString(10, y, f"Nº Pedido: #{pedido.id}")
    y -= 15
    p.drawString(10, y, f"Data: {localtime(pedido.criado_em).strftime('%d/%m/%Y %H:%M')}")
    y -= 20

    # Itens do pedido
    p.drawString(10, y, "Itens:")
    y -= 15
    for item in pedido.itens.all():
        preco = float(item.produto.preco) * item.quantidade
        p.drawString(10, y, f"{item.quantidade}x {item.produto.nome}")
        p.drawRightString(width_pt - 10, y, f"R$ {preco:.2f}")
        y -= 12

    y -= 5
    p.line(10, y, width_pt - 10, y)
    y -= 15

    # Total
    total = float(pedido.total()) if callable(pedido.total) else float(pedido.total)
    p.setFont("Helvetica-Bold", 9)
    p.drawString(10, y, "Total:")
    p.drawRightString(width_pt - 10, y, f"R$ {total:.2f}")
    y -= 20

    # Pagamento
    p.setFont("Helvetica", 8)
    if pagamento:
        metodo = pagamento.get_metodo_pagamento_display().upper()
        p.drawString(10, y, f"Pagamento: {metodo}")
        y -= 15

        if pagamento.valor_recebido:
            p.drawString(10, y, f"Recebido:")
            p.drawRightString(width_pt - 10, y, f"R$ {pagamento.valor_recebido:.2f}")
            y -= 15

        if pagamento.troco:
            p.drawString(10, y, "Troco:")
            p.drawRightString(width_pt - 10, y, f"R$ {pagamento.troco:.2f}")
            y -= 15
    else:
        p.drawString(10, y, "Pagamento: -")
        y -= 15

    # Agradecimento
    y -= 10
    p.setFont("Helvetica-Oblique", 8)
    p.drawCentredString(width_pt / 2, y, "Obrigado pela preferência!")

    # Finalizar PDF
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=False, filename=f"comprovante_pedido_{pedido.id}.pdf")




def confirmacao_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "caixa/confirmacao_pagamento.html", {"pedido": pedido})
