from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import localtime
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.utils.timezone import now
from decimal import Decimal
from pedidos.models import Pedido
from restaurantes.models import Mesa
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




def registrar_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if pedido.status != "PE":
        return redirect("caixa")

    if request.method == "POST":
        metodo_pagamento = request.POST.get("metodo_pagamento")
        valor_recebido = Decimal(request.POST.get("valor_recebido") or "0.00")

        valor_total = sum(item.produto.preco * item.quantidade for item in pedido.itens.all())
        troco = max(valor_recebido - Decimal(valor_total), Decimal("0.00"))

        pagamento = Pagamento.objects.create(
            pedido=pedido,
            valor_total=valor_total,
            valor_recebido=valor_recebido,
            troco=troco,
            metodo_pagamento=metodo_pagamento,
            pago=True,
            data_pagamento=now(),
        )

        pedido.status = "FI"  # Finalizado
        pedido.save()

        return redirect("confirmacao_pagamento", pedido_id=pedido.id)

    return render(request, "caixa/registrar_pagamento.html", {"pedido": pedido})




def detalhe_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == "POST":
        metodo_pagamento = request.POST.get("metodo_pagamento")
        valor_recebido_input = request.POST.get("valor_recebido")

        valor_total = pedido.total()

        # Se for dinheiro, o valor recebido precisa ser maior ou igual
        if metodo_pagamento == "dinheiro":
            valor_recebido = Decimal(valor_recebido_input) if valor_recebido_input else Decimal("0.00")
        else:
            valor_recebido = valor_total  # Cartão ou Pix sempre igual ao valor total

        # Cria e salva pagamento
        pagamento = Pagamento.objects.create(
            pedido=pedido,
            valor_total=valor_total,
            valor_recebido=valor_recebido,
            metodo_pagamento=metodo_pagamento,
            pago=True,
        )

        # Atualiza status do pedido
        pedido.status = Pedido.Status.PAGO
        pedido.save()

        return render(request, "caixa/recibo.html", {
            "pedido": pedido,
            "pagamento": pagamento,
            "troco": pagamento.troco
        })

    return render(request, "caixa/registrar_pagamento.html", {
        "pedido": pedido,
        "valor_total": pedido.total()
    })




def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "caixa/detalhe_pedido.html", {"pedido": pedido})





def gerar_comprovante(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)

    buffer = BytesIO()

    # Tamanho típico de uma impressora térmica: 80mm x 200mm
    width_mm = 80
    height_mm = 200
    width_pt = width_mm * 2.83  # 1 mm ≈ 2.83 pt
    height_pt = height_mm * 2.83

    p = canvas.Canvas(buffer, pagesize=(width_pt, height_pt))
    y = height_pt - 20

    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width_pt / 2, y, "Restaurante Exemplo")
    y -= 20

    p.setFont("Helvetica", 8)
    p.drawString(10, y, f"Nº Pedido: #{pedido.id}")
    y -= 15
    p.drawString(10, y, f"Data: {localtime(pedido.criado_em).strftime('%d/%m/%Y %H:%M')}")
    y -= 20

    p.drawString(10, y, "Itens:")
    y -= 15

    for item in pedido.itens.all():
        p.drawString(10, y, f"{item.quantidade}x {item.produto.nome}")
        y -= 12
        # Verifique se item.produto.preco é numérico e formate corretamente
        preco = float(item.produto.preco) * item.quantidade
        p.drawRightString(width_pt - 10, y + 12, f"R$ {preco:.2f}")

    y -= 10
    p.line(10, y, width_pt - 10, y)
    y -= 15
    p.setFont("Helvetica-Bold", 9)
    p.drawString(10, y, "Total:")
    
    # Verifique se pedido.total é realmente um número
    try:
        total = float(pedido.total)  # Certifique-se de que é um número
    except (ValueError, TypeError):
        total = 0.0  # Caso o total não seja um número válido, defina como 0.0

    p.drawRightString(width_pt - 10, y, f"R$ {total:.2f}")

    y -= 20
    p.setFont("Helvetica", 8)
    if hasattr(pedido, 'pagamento'):
        metodo_pagamento = pedido.pagamento.get_metodo_pagamento_display() if pedido.pagamento.metodo_pagamento else 'Não especificado'
        p.drawString(10, y, f"Pagamento: {metodo_pagamento.upper()}")
    else:
        p.drawString(10, y, "Pagamento: -")

    y -= 25
    p.drawCentredString(width_pt / 2, y, "Obrigado pela preferência!")

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=False, filename=f"comprovante_pedido_{pedido.id}.pdf")




def confirmacao_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "caixa/confirmacao_pagamento.html", {"pedido": pedido})
