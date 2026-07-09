from django import forms

from .models import MessageBoardPost


class MessageBoardPostForm(forms.ModelForm):
    class Meta:
        model = MessageBoardPost
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "maxlength": 280}),
        }
