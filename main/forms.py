from django import forms
from django.forms import ModelForm
from main.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured", "stock", "brand"]

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
    
    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        if sale_price and sale_price < 0:
            raise forms.ValidationError("Sale price cannot be negative.")
        return sale_price
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        sale_price = cleaned_data.get('sale_price')
        
        if sale_price and price and sale_price >= price:
            raise forms.ValidationError("Sale price must be lower than regular price.")
        
        return cleaned_data