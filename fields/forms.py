from django import forms
from .models import Field, CropHistory


class FieldForm(forms.ModelForm):
    """
    Form for creating and editing Field instances
    """
    class Meta:
        model = Field
        fields = ['name', 'location', 'size_acres', 'soil_type', 'irrigation_type', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., North Field A'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 40.7128° N, 74.0060° W'
            }),
            'size_acres': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 25.5',
                'step': '0.01',
                'min': '0.01'
            }),
            'soil_type': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'irrigation_type': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional notes about the field...'
            }),
        }
        labels = {
            'name': 'Field Name',
            'location': 'Location',
            'size_acres': 'Size (acres)',
            'soil_type': 'Soil Type',
            'irrigation_type': 'Irrigation Type',
            'notes': 'Notes',
        }


class CropHistoryForm(forms.ModelForm):
    """
    Form for creating and editing CropHistory instances
    """
    class Meta:
        model = CropHistory
        fields = [
            'field', 'crop_name', 'variety', 'planting_date', 'harvest_date',
            'yield_amount', 'fertilizer_used', 'pesticide_used',
            'weather_conditions', 'notes'
        ]
        widgets = {
            'field': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'crop_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Wheat, Corn, Soybeans'
            }),
            'variety': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Golden Harvest 2000'
            }),
            'planting_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'harvest_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'yield_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'kg per acre',
                'step': '0.01',
                'min': '0'
            }),
            'fertilizer_used': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., NPK 10-10-10'
            }),
            'pesticide_used': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Glyphosate'
            }),
            'weather_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notable weather during growing season...'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional observations...'
            }),
        }
        labels = {
            'field': 'Field',
            'crop_name': 'Crop Name',
            'variety': 'Variety/Cultivar',
            'planting_date': 'Planting Date',
            'harvest_date': 'Harvest Date',
            'yield_amount': 'Yield (kg/acre)',
            'fertilizer_used': 'Fertilizers Used',
            'pesticide_used': 'Pesticides Used',
            'weather_conditions': 'Weather Conditions',
            'notes': 'Notes',
        }
    
    def clean(self):
        """
        Validate that harvest date is after planting date
        """
        cleaned_data = super().clean()
        planting_date = cleaned_data.get('planting_date')
        harvest_date = cleaned_data.get('harvest_date')
        
        if planting_date and harvest_date:
            if harvest_date <= planting_date:
                raise forms.ValidationError(
                    "Harvest date must be after planting date."
                )
        
        return cleaned_data
