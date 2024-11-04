# blog/forms.py
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, 
        widget=forms.TextInput(attrs={'class': 'w-full p-2 bg-gray-700 rounded'}))
    email = forms.EmailField(required=False,
        widget=forms.EmailInput(attrs={'class': 'w-full p-2 bg-gray-700 rounded'}))
    website = forms.URLField(required=False,
        widget=forms.URLInput(attrs={'class': 'w-full p-2 bg-gray-700 rounded'}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 bg-gray-700 rounded',
            'rows': 4,
            'placeholder': 'Write your comment here...'
        }))
    
class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Search posts...',
                'aria-label': 'Search'
            }
        )
    )