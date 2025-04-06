from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CaixaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("painel_caixa", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("painel_caixa", self.channel_name)

    async def receber_pedido(self, event):
        await self.send(text_data=json.dumps(event["pedido"]))
