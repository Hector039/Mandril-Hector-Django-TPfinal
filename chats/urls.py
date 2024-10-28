from django.urls import path
from .views import getUserMsgs

urlpatterns = [
    path('msg-detail/<int:uid>/', getUserMsgs, name='msg-detail'),
    path('msg-detail/', getUserMsgs, name='msg-detail'),
]