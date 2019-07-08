import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import ChatRoom, Message
from .serializers import MessageSerializer

class ChatConsumer(WebsocketConsumer):
    def create_message(self, data):
        message = Message.objects.create_from_username_and_chatroom(
            content = data['message'],
            username = data['sender'],
            chatroom = data['chatroom']
        )
        content = {
            'command': 'messages',
            'messages': [MessageSerializer(message).data]
        }
        self.send_chat_message(content)

    def fetch_messages_to_json(self, data):
        messages = ChatRoom.objects.get(room_name = data['chatroom']).last_messages(20)
        json_messages = []

        for m in messages:
            json_messages.append(MessageSerializer(m).data)

        content = {
            'command': 'messages',
            'messages': json_messages
        }
        self.send(json.dumps(content))
    #
    commands = {
        'fetch': fetch_messages_to_json,
        'create': create_message
    }
    #
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        message = ""
        if data['command'] != 'fetch':
            message = data['message']
        self.commands[data['command']](self, data)
        # Send message to room group

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'messagex': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['messagex']
        print(event)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
    #
    # def send_message(self, message):
    #     self.send(text_data=json.dumps(message))
