
from django.db import models
import qrcode
import time
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import User

class Restaurante(models.Model):
    nome = models.CharField(max_length=200) #nome do restaurante
    dono = models.ForeignKey(User, on_delete=models.CASCADE) #relacionado ao dono
    cnpj = models.CharField(max_length=18, unique=True) #cnpj unico


    def __str__(self):
        return self.nome


class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Salva o objeto primeiro para garantir que ele tenha um ID
        super().save(*args, **kwargs)

        # Gerar URL única da mesa (substitua pelo domínio real do seu sistema)
        url_mesa = f"http://127.0.0.1:8000/pedido/mesa/{self.numero}"

        # Gerar QR Code
        qr = qrcode.make(url_mesa)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        # Criar um nome de arquivo válido
        file_name = f"mesa_{self.numero}_{int(time.time())}.png"

        # Salvar o QR Code no campo do modelo
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

        # Salvar novamente para garantir que o QR Code seja persistido
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Mesa {self.numero}"
    


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)  # Opcional

    def __str__(self):
        return self.nome