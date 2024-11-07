# blog/forms.py
from django import forms
from .models import Comment
from django.core.exceptions import ValidationError

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

        def clean_content(self):
            content = self.cleaned_data['content']
            if len(content) < 3:
                raise ValidationError('Comment is too short')
            return content