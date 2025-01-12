from django import forms
from .models import InventoryItem, Brand, Category, Warehouse, GlobalSettings
from django.db import transaction
from django.core.exceptions import ValidationError

class InventoryItemForm(forms.ModelForm):
    create_in_both = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = InventoryItem
        fields = ['brand', 'category', 'model', 'item_name', 'price', 'stock', 'warehouse', 'image']
        widgets = {
            'model': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True,
                'placeholder': 'Enter model number or name'
            }),
            'item_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True,
                'placeholder': 'Enter item name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True,
                'min': '0.01',
                'step': '0.01',
                'placeholder': 'Enter price'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True,
                'min': '0',
                'step': '1',
                'placeholder': 'Enter stock quantity'
            }),
            'image': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set required fields
        for field in ['brand', 'category', 'model', 'item_name', 'price', 'stock', 'warehouse']:
            self.fields[field].required = True
        
        # Add help text
        self.fields['image'].help_text = 'Upload an image of the item (optional)'
        
        # Set up brand and category fields
        self.fields['brand'] = forms.ModelChoiceField(
            queryset=Brand.objects.all(),
            empty_label="Select a brand",
            widget=forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True
            })
        )
        
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            empty_label="Select a category",
            widget=forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True
            })
        )
        
        # Create warehouse field with choices
        self.fields['warehouse'] = forms.ChoiceField(
            choices=[('', 'Select a warehouse')],
            widget=forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True
            })
        )
        
        # Filter warehouse choices based on user role
        if self.user and hasattr(self.user, 'customuser'):
            user_role = self.user.customuser.role
            choices = [('', 'Select a warehouse'), ('both', 'Both Warehouses')]
            
            if user_role == 'attendant':
                attendant_warehouse = Warehouse.objects.get(name='Attendant Warehouse')
                choices.append((str(attendant_warehouse.id), 'Attendant Warehouse'))
            elif user_role == 'manager':
                manager_warehouse = Warehouse.objects.get(name='Manager Warehouse')
                choices.append((str(manager_warehouse.id), 'Manager Warehouse'))
            elif self.user.is_superuser:
                for warehouse in Warehouse.objects.all():
                    choices.append((str(warehouse.id), warehouse.name))
            
            self.fields['warehouse'].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        warehouse_choice = cleaned_data.get('warehouse')
        model = cleaned_data.get('model')
        brand = cleaned_data.get('brand')

        # Call the model's clean method to validate unique model per brand
        if brand and model:
            instance = self.instance if self.instance.pk else InventoryItem()
            instance.brand = brand
            instance.model = model
            try:
                instance.clean()
            except ValidationError as e:
                # Add the error to the form
                if 'model' in e.error_dict:
                    self.add_error('model', e.error_dict['model'])

        # Handle warehouse choice
        if warehouse_choice == 'both':
            cleaned_data['create_in_both'] = True
            try:
                cleaned_data['warehouse'] = Warehouse.objects.get(name='Manager Warehouse')
            except Warehouse.DoesNotExist:
                raise forms.ValidationError("Manager Warehouse does not exist")
        else:
            cleaned_data['create_in_both'] = False
            try:
                cleaned_data['warehouse'] = Warehouse.objects.get(id=int(warehouse_choice))
            except (Warehouse.DoesNotExist, ValueError):
                raise forms.ValidationError("Please select a valid warehouse")
        
        return cleaned_data

class StockEditForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['stock']
        widgets = {
            'stock': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True,
                'min': '0',
                'step': '1',
                'placeholder': 'Enter stock quantity'
            })
        }

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ['reorder_level']
        widgets = {
            'reorder_level': forms.NumberInput(attrs={
                'class': 'pl-3 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'min': '1',
                'step': '1',
                'placeholder': 'Enter reorder level',
                'required': True
            })
        }
        
    def clean_reorder_level(self):
        reorder_level = self.cleaned_data.get('reorder_level')
        if reorder_level is not None:
            if reorder_level < 1:
                raise forms.ValidationError("Reorder level must be at least 1")
        return reorder_level

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class LimitedInventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['stock', 'image']
        widgets = {
            'stock': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
                'required': True,
                'min': '0',
                'step': '1',
                'placeholder': 'Enter stock quantity'
            }),
            'image': forms.FileInput(attrs={
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image'].help_text = 'Upload an image of the item (optional)'