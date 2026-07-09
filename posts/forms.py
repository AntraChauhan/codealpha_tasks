from django import forms
from .models import Post, Comment, Message


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Type a message..."
            })
        }