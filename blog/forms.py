# blog/forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 bg-gray-800 rounded-lg',
                'placeholder': 'not required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2 bg-gray-800 rounded-lg',
                'placeholder': 'optional and will not be published'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 bg-gray-800 rounded-lg',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }