from django.urls import path
from .views import sendMsg, getUserChats, getUserMsgs

urlpatterns = [
    path('msg-send/<int:uid>/', sendMsg, name='msg-send'),
    path('my-msgs/', getUserChats, name='my-msgs'),
    path('msg-detail/<int:uid>/', getUserMsgs, name='msg-detail'),
]