from django.forms import ModelForm
from .models import Message
from django.forms import TextInput

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Message:'
                })
        }
        labels = {
            "message": ""
        }