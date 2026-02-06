from django import forms
from .models import FinancialRecord, PerformanceMetric, YieldForecast, Report
from fields.models import Field
from datetime import datetime


class FinancialRecordForm(forms.ModelForm):
    """Form for creating and editing financial records"""
    
    class Meta:
        model = FinancialRecord
        fields = [
            'field', 'crop_history', 'transaction_type', 'category', 'amount',
            'date', 'description', 'quantity', 'unit', 'vendor_buyer',
            'invoice_number', 'payment_method', 'is_recurring', 'notes'
        ]
        
        widgets = {
            'field': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select field (optional)'
            }),
            'crop_history': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select related crop history (optional)'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detailed description of the transaction'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity (optional)',
                'step': '0.01'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., kg, liters, bags'
            }),
            'vendor_buyer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Vendor or buyer name'
            }),
            'invoice_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Invoice/receipt number'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes'
            }),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount


class YieldForecastForm(forms.ModelForm):
    """Form for creating and editing yield forecasts"""
    
    class Meta:
        model = YieldForecast
        fields = [
            'field', 'crop_name', 'forecast_year', 'planting_season',
            'predicted_yield_kg', 'confidence_level', 'prediction_method',
            'actual_yield_kg', 'notes'
        ]
        
        widgets = {
            'field': forms.Select(attrs={
                'class': 'form-control'
            }),
            'crop_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Wheat, Corn, Soybeans',
                'list': 'crop-suggestions'
            }),
            'forecast_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': datetime.now().year,
                'max': datetime.now().year + 10,
                'placeholder': str(datetime.now().year)
            }),
            'planting_season': forms.Select(attrs={
                'class': 'form-control'
            }),
            'predicted_yield_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Predicted total yield in kg',
                'step': '0.01',
                'min': '0'
            }),
            'confidence_level': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'placeholder': '0-100%'
            }),
            'prediction_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'actual_yield_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Actual yield (after harvest)',
                'step': '0.01',
                'min': '0'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about the forecast'
            }),
        }
    
    def clean_forecast_year(self):
        year = self.cleaned_data.get('forecast_year')
        if year and year < datetime.now().year:
            raise forms.ValidationError("Forecast year cannot be in the past.")
        return year


class ReportGeneratorForm(forms.Form):
    """Form for generating analytics reports"""
    
    report_type = forms.ChoiceField(
        choices=Report.REPORT_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        help_text="Type of report to generate"
    )
    
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Report title'
        }),
        help_text="Custom title for the report"
    )
    
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text="Report period start date"
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text="Report period end date"
    )
    
    fields = forms.ModelMultipleChoiceField(
        queryset=Field.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        help_text="Select fields to include in the report"
    )
    
    include_charts = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        help_text="Include charts and visualizations"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("Start date must be before end date.")
        
        return cleaned_data


class DateRangeFilterForm(forms.Form):
    """Form for filtering data by date range"""
    
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Start date'
        })
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'End date'
        })
    )
    
    field = forms.ModelChoiceField(
        queryset=Field.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        empty_label="All Fields"
    )
