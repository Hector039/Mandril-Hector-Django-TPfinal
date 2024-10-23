from django.urls import path
from .views import sendMsg, getUserMsgs

urlpatterns = [
    path('msg-send/<int:uid>/', sendMsg, name='msg-send'),
    path('msg-detail/<int:uid>/', getUserMsgs, name='msg-detail'),
    path('msg-detail/', getUserMsgs, name='msg-detail'),
]