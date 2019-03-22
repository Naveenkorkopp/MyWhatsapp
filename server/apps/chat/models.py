from django.db import models


class ChatModel(models.Model):
    # To save the chat logs for a particular chat room
    chat_group_name = models.CharField(max_length=100)
    chat_log = models.TextField()

    def __str__(self):
        return self.chat_group_name
