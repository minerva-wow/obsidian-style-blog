# blog/forms.py
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, 
        widget=forms.TextInput(attrs={'class': 'w-full p-2 bg-gray-800 rounded-lg'}))
    email = forms.EmailField(required=False,
        widget=forms.EmailInput(attrs={'class': 'w-full p-2 bg-gray-800 rounded-lg'}))
    website = forms.URLField(required=False,
        widget=forms.URLInput(attrs={'class': 'w-full p-2 bg-gray-800 rounded-lg'}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 bg-gray-800 rounded-lg',
            'rows': 4,
            'placeholder': 'Write your comment here...'
        }))