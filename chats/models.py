from django.db import models
from users.models import CustomUser

class ChatRegister(models.Model):
        user1_id = models.ForeignKey(CustomUser, related_name='user1', on_delete=models.CASCADE)
        user2_id = models.ForeignKey(CustomUser, related_name='user2', on_delete=models.CASCADE)
        class Meta:
            constraints = [models.UniqueConstraint(fields=['user1_id', 'user2_id'], name='unique_chat')]

class Message(models.Model):
    id =            None
    chat_id =       models.ForeignKey(ChatRegister, on_delete=models.CASCADE)
    to_id =         models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_id')
    from_id =       models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_id')
    message =       models.TextField(max_length=240)
    date =          models.DateTimeField(auto_now_add=True)
    seen =          models.BooleanField(default=False)

