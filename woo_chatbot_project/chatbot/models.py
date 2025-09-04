from django.db import models

class ChatMessage(models.Model):
    role = models.CharField(max_length=20)   # "user" or "assistant"
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
