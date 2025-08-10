import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class MarketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'market_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        # Process messages from client (e.g. placing order) if needed
        pass

    async def market_update(self, event):
        # Broadcast market updates to clients
        await self.send_json(event['data'])
