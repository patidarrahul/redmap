from django import forms
from .models import *


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['designation', 'profile_picture']
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Designation'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Profile Picture'}),
        }

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


class SpinStepForm(forms.ModelForm):
    class Meta:
        model = SpinStep
        fields = ('spin_speed', 'spin_time', 'spin_acceleration')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["spin_speed"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter spin speed in rpm"})
        self.fields["spin_time"].widget.attrs.update(
            {"class": "form-control",  "placeholder": "Enter spin time in seconds"})
        self.fields["spin_acceleration"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter spin acceleration in rpm"})


class SpinProgramForm(forms.ModelForm):
    class Meta:
        model = SpinProgram
        fields = ('name', 'program')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Give a name to the program"})
        self.fields["program"].widget.attrs.update(
            {"class": "form-select", "placeholder": "Select spin steps"})
        
class AddStackForm(forms.ModelForm):
    class Meta:
        model = Stack
        fields = ['name', 'geometry', 'substrate',
                  'number_of_layers', 'number_of_devices',  'created', 'experiment']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'substrate': forms.Select(attrs={'class': 'form-select', 'id': 'substrate'}),
            'geometry': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'number_of_layers': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'created': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_devices': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'experiment': forms.Select(attrs={'class': 'form-select', 'required': 'required'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['substrate'].queryset = Inventory.objects.filter(
            item__category__name='Substrate')
        

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title',  'description', 'collaborators', 'created']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 200px;'}),
            'collaborators': forms.SelectMultiple(attrs={'class': 'form-select', 'style': 'height: 200px;'}),
            'created': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['objective', 'notes', 'created']

        widgets = {
            'objective': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'created': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})

        }