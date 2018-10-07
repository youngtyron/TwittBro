from django import forms
from .models import Message, Chat, ImageMessage


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
                'text' : forms.Textarea(attrs = {'class':'form-control', 'rows': 2, 'cols' : 1}),
        }

class ImageMessageForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
