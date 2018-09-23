from django import forms
from .models import Message, Chat, ImageMessage


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
                'text' : forms.Textarea(attrs = {'class':'form-control', 'rows': 2, 'cols' : 1}),
        }
class MakeChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'pict']
        widgets = {
                'name' : forms.Textarea(attrs = {'class':'form-control', 'rows': 1, 'cols' : 1}),
                'pict' : forms.ClearableFileInput()
        }

class ImageMessageForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
