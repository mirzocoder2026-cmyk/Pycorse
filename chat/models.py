from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    slug        = models.SlugField(unique=True)
    name        = models.CharField(max_length=100)
    icon        = models.CharField(max_length=10, default='💬')
    description = models.CharField(max_length=200, blank=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Чатхона'
        verbose_name_plural = 'Чатхонаҳо'

    def __str__(self): return self.name

class Message(models.Model):
    room       = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Паём'
        verbose_name_plural = 'Паёмҳо'

    def __str__(self): return f'{self.user}: {self.content[:40]}'
