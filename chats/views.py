from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as info
from users.models import CustomUser
from .models import Message, ChatRegister
from .forms import MessageForm
from django.db.models import Q

@login_required
def getUserChats(req):
    try:
        userLogued = get_object_or_404(CustomUser, pk=req.user.id).avatar.url if req.user.id else '#'
        chats = ChatRegister.objects.filter(Q(user1_id=req.user.id) | Q(user2_id=req.user.id))
        
        return render(req, "my-msgs.html", {"avatar_url": userLogued, "chats": chats})
    except Exception as error:
        info.error(req, error)
        return render(req, "my-msgs.html", {"avatar_url": userLogued})
    
@login_required
def sendMsg(req, uid):
    fromUser = get_object_or_404(CustomUser, pk=req.user.id)
    userLogued = fromUser.avatar.url if req.user.id else '#'
    toUser = get_object_or_404(CustomUser, pk=uid)
    messageForm = MessageForm()
    if req.method == 'POST':
        try:
            chat = ChatRegister.objects.filter(Q(user1_id=fromUser, user2_id=toUser) | Q(user1_id=toUser, user2_id=fromUser))
            if len(chat) == 0:
                newChat = ChatRegister.objects.create(user1_id=fromUser, user2_id=toUser)            
                Message.objects.create(chat_id=newChat, to_id=toUser, from_id=fromUser, message=req.POST["message"])
                info.success(req, "Message send!")
                return render(req, "msg-send.html", {"avatar_url": userLogued, "form": messageForm, "to": toUser.id, "to_user": f"{toUser.first_name} {toUser.last_name}:"})
                
            Message.objects.create(chat_id = chat[0], to_id=toUser, from_id=fromUser, message=req.POST["message"])
            info.success(req, "Message send!")
            return render(req, "msg-send.html", {"avatar_url": userLogued, "form": messageForm, "to": toUser.id, "to_user": f"{toUser.first_name} {toUser.last_name}:"})
        except Exception as error:
            info.error(req, error)
            return render(req, "msg-send.html", {"avatar_url": userLogued, "form": messageForm, "to": toUser.id, "to_user": f"{toUser.first_name} {toUser.last_name}:"})
  
    return render(req, "msg-send.html", {"avatar_url": userLogued, "form": messageForm, "to": toUser.id, "to_user": f"{toUser.first_name} {toUser.last_name}:"})

@login_required
def getUserMsgs(req, uid):
    try:
        fromUser = get_object_or_404(CustomUser, pk=req.user.id)
        userLogued = fromUser.avatar.url if req.user.id else '#'
        toUser = get_object_or_404(CustomUser, pk=uid)
        messageForm = MessageForm()
        if req.method == 'POST':
            chat = ChatRegister.objects.get(Q(user1_id=fromUser, user2_id=toUser) | Q(user1_id=toUser, user2_id=fromUser))
            Message.objects.create(chat_id=chat, to_id=toUser, from_id=fromUser, message=req.POST["message"])
            messages = Message.objects.filter(Q(to_id=fromUser, from_id=toUser) | Q(to_id=toUser, from_id=fromUser)).order_by('date')

            info.success(req, "Message send!")
            return render(req, "msg-detail.html", {"avatar_url": userLogued, "form": messageForm, "chats": messages, "to": toUser.id, "to_user": f"{toUser.first_name} {toUser.last_name}:"})
        
        messages = Message.objects.filter(Q(to_id=fromUser, from_id=toUser) | Q(to_id=toUser, from_id=fromUser)).order_by('date')

        chat = ChatRegister.objects.get(Q(user1_id=fromUser, user2_id=toUser) | Q(user1_id=toUser, user2_id=fromUser))
        Message.objects.filter(Q(chat_id=chat, to_id=fromUser, seen=False)).update(seen=True)

        return render(req, "msg-detail.html", {"avatar_url": userLogued, "form": messageForm, "chats": messages, "to": toUser.id, "to_user": f"{toUser.first_name} {toUser.last_name}:"})
    except Exception as error:
        info.error(req, error)
        return render(req, "msg-detail.html", {"avatar_url": userLogued, "form": messageForm})