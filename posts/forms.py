from django import forms
from .models import  Post, Comment, ImagePost

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs = {'class':'form-control', 'rows': 3, 'cols' : 2}),
         }

class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs = {'class' : 'form-control', 'rows':2, 'cols':2}),
        }

class ImagePostForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
