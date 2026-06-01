from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import ChatRoom, Message

@login_required
def chat_view(request, slug='general'):
    rooms   = ChatRoom.objects.filter(is_active=True)
    room    = get_object_or_404(ChatRoom, slug=slug)
    msgs    = Message.objects.filter(room=room, is_deleted=False).select_related('user').order_by('-created_at')[:60]
    return render(request, 'chat/chat.html', {
        'rooms': rooms, 'room': room, 'messages': list(reversed(msgs))
    })

@login_required
@require_POST
def send_message(request):
    data    = json.loads(request.body)
    slug    = data.get('room','general')
    content = data.get('content','').strip()[:1000]
    if not content:
        return JsonResponse({'ok': False})
    room = get_object_or_404(ChatRoom, slug=slug)
    msg  = Message.objects.create(user=request.user, room=room, content=content)
    return JsonResponse({'ok': True, 'msg': {
        'id':   msg.id,
        'user': str(request.user),
        'text': msg.content,
        'time': msg.created_at.strftime('%H:%M'),
    }})

@login_required
def poll_messages(request, slug):
    last_id = int(request.GET.get('last',0))
    room    = get_object_or_404(ChatRoom, slug=slug)
    msgs    = Message.objects.filter(room=room, id__gt=last_id, is_deleted=False).select_related('user').order_by('created_at')
    return JsonResponse({'msgs': [{
        'id':   m.id, 'user': str(m.user),
        'text': m.content, 'time': m.created_at.strftime('%H:%M'),
        'me':   m.user == request.user,
    } for m in msgs]})
