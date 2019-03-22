from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import logging
from .models import ChatModel
from .serializers import ChatModelSerializer

logger = logging.getLogger()


class ChatConsumer(WebsocketConsumer):

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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'group_name': self.room_group_name,
            }
        )

    # Receive message from room group
    def chat_message(self, event):

        message = event['message']
        group_name = event['group_name']

        chat_model_obj = ChatModel.objects.all()

        flag = False

        for chat in chat_model_obj:
            if chat.chat_group_name == group_name:
                chat.chat_log += str(message + '\n')
                chat.save()
                flag = True

        if not flag:
            new_chat_obj = ChatModel()
            new_chat_obj.chat_group_name = group_name
            new_chat_obj.chat_log = message
            new_chat_obj.save()

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'chat_models': ChatModelSerializer(chat_model_obj, many=True).data,
        }))
