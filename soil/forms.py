from django import forms
from .models import SoilAnalysis, NutrientRecommendation


class SoilAnalysisForm(forms.ModelForm):
    """
    Form for creating and editing SoilAnalysis instances
    """
    class Meta:
        model = SoilAnalysis
        fields = [
            'field', 'analysis_date', 'ph_level', 'organic_matter',
            'nitrogen_ppm', 'phosphorus_ppm', 'potassium_ppm',
            'calcium_ppm', 'magnesium_ppm', 'sulfur_ppm',
            'cec', 'moisture_content', 'lab_name', 'notes'
        ]
        widgets = {
            'field': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'analysis_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'ph_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 6.5',
                'step': '0.1',
                'min': '0',
                'max': '14'
            }),
            'organic_matter': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3.5',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'nitrogen_ppm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ppm',
                'step': '0.01',
                'min': '0'
            }),
            'phosphorus_ppm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ppm',
                'step': '0.01',
                'min': '0'
            }),
            'potassium_ppm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ppm',
                'step': '0.01',
                'min': '0'
            }),
            'calcium_ppm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ppm (optional)',
                'step': '0.01',
                'min': '0'
            }),
            'magnesium_ppm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ppm (optional)',
                'step': '0.01',
                'min': '0'
            }),
            'sulfur_ppm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ppm (optional)',
                'step': '0.01',
                'min': '0'
            }),
            'cec': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'meq/100g (optional)',
                'step': '0.01',
                'min': '0'
            }),
            'moisture_content': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '% (optional)',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'lab_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., AgriTest Labs'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional observations...'
            }),
        }
        labels = {
            'field': 'Field',
            'analysis_date': 'Analysis Date',
            'ph_level': 'pH Level (0-14)',
            'organic_matter': 'Organic Matter (%)',
            'nitrogen_ppm': 'Nitrogen (ppm)',
            'phosphorus_ppm': 'Phosphorus (ppm)',
            'potassium_ppm': 'Potassium (ppm)',
            'calcium_ppm': 'Calcium (ppm)',
            'magnesium_ppm': 'Magnesium (ppm)',
            'sulfur_ppm': 'Sulfur (ppm)',
            'cec': 'CEC (meq/100g)',
            'moisture_content': 'Moisture Content (%)',
            'lab_name': 'Laboratory Name',
            'notes': 'Notes',
        }


class NutrientRecommendationForm(forms.ModelForm):
    """
    Form for creating nutrient recommendations
    """
    class Meta:
        model = NutrientRecommendation
        fields = ['soil_analysis', 'nutrient', 'current_level', 'recommended_action', 'application_rate', 'priority']
        widgets = {
            'soil_analysis': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'nutrient': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'current_level': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'recommended_action': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the recommended action...'
            }),
            'application_rate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 50 kg/acre'
            }),
            'priority': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            }),
        }
        labels = {
            'soil_analysis': 'Soil Analysis',
            'nutrient': 'Nutrient/Parameter',
            'current_level': 'Current Level',
            'recommended_action': 'Recommended Action',
            'application_rate': 'Application Rate',
            'priority': 'Priority (1-10)',
        }
