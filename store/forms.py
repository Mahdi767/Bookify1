# store/forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['created_at']
        fields = ['title', 'author', 'description', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 pl-10 pr-3 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'e.g., The Great Gatsby'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 pl-10 pr-3 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'e.g., F. Scott Fitzgerald'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 pl-10 pr-3 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'e.g., 19.99'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 px-3 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'A short summary of the book...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'sr-only' 
            }),
        }