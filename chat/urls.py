from django.urls import path
from . import views
urlpatterns = [
    path('',                views.chat_view,      name='chat'),
    path('<slug:slug>/',    views.chat_view,       name='chat_room'),
    path('api/send/',       views.send_message,    name='chat_send'),
    path('api/poll/<slug:slug>/', views.poll_messages, name='chat_poll'),
]
