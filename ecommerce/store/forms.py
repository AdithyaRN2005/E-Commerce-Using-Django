from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category','title','description','price','image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-4 border border-gray-400'
        }),
        'title': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-400'

        }),
        'description': forms.Textarea(attrs={
                'class': 'w-full p-4 border border-gray-400'

        }),
        'price': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-400'

        }),
        'image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-400'

        }),
        }