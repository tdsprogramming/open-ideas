from django.db import models
from django.contrib.auth import get_user_model

from django_extensions.db.models import TimeStampedModel

User = get_user_model()

class ChatRoomManager(models.Manager):
    def create_or_get_with_users(self, user1, user2):
        room_name = "{}-{}".format(user1.username, user2.username)
        existing_chatroom = self.get_with_users(user1, user2)

        if existing_chatroom:
            chatroom = existing_chatroom
        else:
            chatroom = self.create(
                room_name = room_name
            )
            chatroom.users.add(user1, user2)
        return chatroom

    def get_with_users(self, user1, user2):
        rooms = self.filter(room_name__contains = user1.username).filter(room_name__contains = user2.username)

        if rooms:
            return rooms.first()
        return False

class ChatRoom(models.Model):
    users = models.ManyToManyField(User)
    room_name = models.CharField(max_length = 1500)

    objects = ChatRoomManager()

    def last_messages(self, number):
        return reversed(Message.objects.filter(chatroom = self).order_by('-created')[:number])

class MessageManager(models.Manager):
    def create_from_username_and_chatroom(self, content, username, chatroom):
        sender = User.objects.get(username=username)
        chatroom = ChatRoom.objects.get(room_name = chatroom)
        return self.create(
            content = content,
            sender = sender,
            chatroom = chatroom
        )


class Message(TimeStampedModel):
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete = models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete = models.CASCADE)

    objects = MessageManager()
