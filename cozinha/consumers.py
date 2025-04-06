from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CozinhaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("cozinha", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("cozinha", self.channel_name)

    async def novo_pedido(self, event):
        await self.send(text_data=json.dumps({
            "type": "novo_pedido",
            "pedido": event["pedido"]
        }))
