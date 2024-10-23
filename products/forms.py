from django.forms import ModelForm
from django import forms
from .models import Product
from django.forms import TextInput, NumberInput, Textarea, Select

category_choices = (
        ('other', 'Other'),
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('accesories', 'Accesories'),
        ('computing', 'Computing'))

class ProductForm(ModelForm):
    category = forms.ChoiceField(choices=category_choices, widget = Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}), label='Category')

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'stock', 'category', 'status']
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                }),
            'description': Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                }),
            'price': NumberInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'step': 0.25
                }),
            'stock': NumberInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                })
        }
        labels = {
            "title": "Title:",
            "description": "Description:",
            "price": "Price:",
            "stock": "Stock:",
        }

class ProductSearchForm(forms.Form):
    
    order_by_price = (
        ("all", 'All'),
        ("ascending", 'Ascending'),
        ("descending", 'Descending'))

    title = forms.CharField(max_length=20, required=False, widget=TextInput(attrs={ 'class': "form-control", 'style': 'max-width: 300px;', 'placeholder': 'Title' }), label='')
    price = forms.ChoiceField(choices=order_by_price, required=False, widget = Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}))
    category = forms.ChoiceField(choices=category_choices, required=False, widget = Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}))