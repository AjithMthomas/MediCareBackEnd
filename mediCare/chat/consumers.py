from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            # Parse the incoming message as JSON
            data = json.loads(text_data)
            message = data.get('message')
            author = data.get('author')
            room_id = data.get('room_id')

            if not (message and author and room_id):
                raise ValueError('Invalid message data')

            # Save the message to the database or perform any desired actions
            # ... (add code here to save the message to the database)

            # Broadcast the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'author': author
                }
            )

        except (json.JSONDecodeError, ValueError) as e:
            # Handle invalid JSON or missing fields
            error_message = {'error': str(e)}
            await self.send(text_data=json.dumps(error_message))

    async def chat_message(self, event):
        message = event['message']
        author = event['author']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author': author
        }))
