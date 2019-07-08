from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('get-chat-room/', views.get_room, name='get_chatroom'),
    path('<str:room_name>/', views.room, name='room')
]
