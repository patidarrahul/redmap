from django import forms
from .models import *


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['item', 'batch', 'arrival_date', 'expiry_date',
                  'total_units', 'unit_size', 'measurement_unit', 'notes']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control mt-2', 'placeholder': 'Slect an item'}),
            'batch': forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Batch Name or Number', 'required': 'required'}),
            'arrival_date': forms.DateInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Arrival Date', 'type': 'date', 'required': 'required'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Expiry Date', 'type': 'date', 'required': 'required'}),
            'total_units': forms.NumberInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Total Units', 'required': 'required'}),
            'unit_size': forms.NumberInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Unit Size', 'required': 'required'}),
            'measurement_unit': forms.Select(attrs={'class': 'form-control mt-2', 'placeholder': 'Measurement Unit', 'required': 'required'}),
            'notes': forms.Textarea(attrs={'class': 'form-control mt-2', 'placeholder': 'Notes'}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'supplier', 'category', 'short_name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Name'}),
            'category': forms.Select(attrs={'class': 'form-control mt-2', 'placeholder': 'Category'}),
            'supplier': forms.Select(attrs={'class': 'form-control mt-2', 'placeholder': 'Supplier'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Short Name'}),
            'type': forms.Select(attrs={'class': 'form-control mt-2', 'placeholder': 'Type'}),
        
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Name'}),
          
        }