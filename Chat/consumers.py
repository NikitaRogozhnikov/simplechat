import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from Chat.models import Chat, Message
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.chat=Chat.objects.get(pk=int(self.room_name))
        mes=[]
        for i in self.chat.message_set.all():
            mes.append(i.messages)

        jmes='\n'.join(mes)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

 
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = self.scope["user"].username+': '+text_data_json['message']
        self.chat.message_set.create(messages=message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    def chat_message(self, event):
        print('event is: ',event)
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
