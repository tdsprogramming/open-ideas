from rest_framework import serializers

from .models import ChatRoom, Message
from accounts.serializers import ClientUserSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = (
            'room_name',
        )
class MessageSerializer(serializers.ModelSerializer):
    chatroom = ChatRoomSerializer(many = False)
    sender = ClientUserSerializer(many = False)
    class Meta:
        model = Message
        fields = (
            'content',
            'chatroom',
            'sender',
            'created'
        )
