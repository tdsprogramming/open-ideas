import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import JsonResponse

from .models import ChatRoom, Message
from accounts.models import ClientUser

def get_room(request):
    current_user_username = request.GET['current_user_username']
    other_user_username = request.GET['other_user_username']
    current_user = ClientUser.objects.filter(username=current_user_username).first()
    other_user = ClientUser.objects.filter(username=other_user_username).first()
    chatroom = ChatRoom.objects.create_or_get_with_users(
        current_user,
        other_user
    )
    return JsonResponse({'room_name':chatroom.room_name})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def create_message_ajax(request):
    content = request.POST['content']
    sender = request.user
    message = Message.objects.create(
         content = content,
         sender = sender
    )
    return render(request, '')
