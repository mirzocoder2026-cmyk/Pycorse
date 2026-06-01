from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name','slug','is_active')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user','room','created_at','is_deleted')
    list_filter  = ('room','is_deleted')
