from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.TextInput(
                attrs={'class': 'p-4 text-black', 'placeholder': 'Type a message ...', 'maxlength': 2000}),
        }
