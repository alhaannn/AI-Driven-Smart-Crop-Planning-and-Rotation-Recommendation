from django import forms
from .models import WeatherData, CropCalendar, CropRecommendation


class WeatherDataForm(forms.ModelForm):
    """
    Form for weather data entry
    """
    class Meta:
        model = WeatherData
        fields = [
            'field', 'date', 'temperature_high', 'temperature_low',
            'rainfall_mm', 'humidity_percent', 'wind_speed_kmh',
            'condition', 'notes'
        ]
        widgets = {
            'field': forms.Select(attrs={'class': 'form-control form-select'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'temperature_high': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '°C',
                'step': '0.1'
            }),
            'temperature_low': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '°C',
                'step': '0.1'
            }),
            'rainfall_mm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'mm',
                'step': '0.01',
                'min': '0'
            }),
            'humidity_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '%',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'wind_speed_kmh': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'km/h',
                'step': '0.01',
                'min': '0'
            }),
            'condition': forms.Select(attrs={'class': 'form-control form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional weather observations...'
            }),
        }
        labels = {
            'field': 'Field',
            'date': 'Date',
            'temperature_high': 'High Temperature (°C)',
            'temperature_low': 'Low Temperature (°C)',
            'rainfall_mm': 'Rainfall (mm)',
            'humidity_percent': 'Humidity (%)',
            'wind_speed_kmh': 'Wind Speed (km/h)',
            'condition': 'Weather Condition',
            'notes': 'Notes',
        }


class CropCalendarForm(forms.ModelForm):
    """
    Form for crop calendar events
    """
    class Meta:
        model = CropCalendar
        fields = [
            'field', 'activity_type', 'crop_name', 'variety',
            'scheduled_date', 'end_date', 'status', 'description',
            'estimated_duration_days', 'recommended_temperature_min',
            'recommended_temperature_max', 'send_reminder',
            'reminder_days_before', 'notes'
        ]
        widgets = {
            'field': forms.Select(attrs={'class': 'form-control form-select'}),
            'activity_type': forms.Select(attrs={'class': 'form-control form-select'}),
            'crop_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Wheat, Corn, Tomato'
            }),
            'variety': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Golden Harvest (optional)'
            }),
            'scheduled_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-control form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detailed activity description...'
            }),
            'estimated_duration_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'days',
                'min': '1'
            }),
            'recommended_temperature_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '°C (optional)',
                'step': '0.1'
            }),
            'recommended_temperature_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '°C (optional)',
                'step': '0.1'
            }),
            'send_reminder': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reminder_days_before': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '30'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...'
            }),
        }
        labels = {
            'field': 'Field',
            'activity_type': 'Activity Type',
            'crop_name': 'Crop Name',
            'variety': 'Variety',
            'scheduled_date': 'Scheduled Date',
            'end_date': 'End Date',
            'status': 'Status',
            'description': 'Description',
            'estimated_duration_days': 'Estimated Duration (days)',
            'recommended_temperature_min': 'Min Temperature (°C)',
            'recommended_temperature_max': 'Max Temperature (°C)',
            'send_reminder': 'Send Reminder',
            'reminder_days_before': 'Reminder Days Before',
            'notes': 'Notes',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        scheduled_date = cleaned_data.get('scheduled_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and scheduled_date and end_date < scheduled_date:
            raise forms.ValidationError("End date cannot be before scheduled date.")
        
        return cleaned_data


class CropRecommendationForm(forms.ModelForm):
    """
    Form for crop recommendations
    """
    class Meta:
        model = CropRecommendation
        fields = [
            'field', 'recommended_crop', 'recommended_variety',
            'planting_season', 'confidence_score', 'reasoning',
            'expected_yield_range', 'ideal_planting_window_start',
            'ideal_planting_window_end'
        ]
        widgets = {
            'field': forms.Select(attrs={'class': 'form-control form-select'}),
            'recommended_crop': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Wheat'
            }),
            'recommended_variety': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., HD-2967 (optional)'
            }),
            'planting_season': forms.Select(attrs={'class': 'form-control form-select'}),
            'confidence_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100'
            }),
            'reasoning': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why this crop is recommended...'
            }),
            'expected_yield_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2000-3000 kg/acre'
            }),
            'ideal_planting_window_start': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'ideal_planting_window_end': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'field': 'Field',
            'recommended_crop': 'Recommended Crop',
            'recommended_variety': 'Recommended Variety',
            'planting_season': 'Best Planting Season',
            'confidence_score': 'Confidence Score (0-100)',
            'reasoning': 'Reasoning',
            'expected_yield_range': 'Expected Yield Range',
            'ideal_planting_window_start': 'Planting Window Start',
            'ideal_planting_window_end': 'Planting Window End',
        }
