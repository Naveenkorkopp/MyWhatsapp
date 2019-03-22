from rest_framework import serializers

from .models import ChatModel


class ChatModelSerializer(serializers.Serializer):
	class Meta:
		model = ChatModel


	def to_representation(self, chat_id):
		data = {
			"chat_group_name" : chat_id.chat_group_name,
			"chat_log" : chat_id.chat_log,
		}

		return data