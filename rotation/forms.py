from django import forms
from .models import RotationPlan, RotationSequence, RotationBenefit
from datetime import datetime


class RotationPlanForm(forms.ModelForm):
    """Form for creating and editing rotation plans"""
    
    class Meta:
        model = RotationPlan
        fields = [
            'field',
            'name',
            'description',
            'start_year',
            'duration_years',
            'status',
            'primary_goal',
            'created_by',
        ]
        widgets = {
            'field': forms.Select(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 4-Year Corn-Soybean Rotation',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the strategy and goals of this rotation plan...',
            }),
            'start_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2000,
                'max': 2100,
                'value': datetime.now().year,
            }),
            'duration_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2,
                'max': 10,
                'value': 4,
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'primary_goal': forms.Select(attrs={
                'class': 'form-control',
            }),
            'created_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)',
            }),
        }
        help_texts = {
            'duration_years': 'Recommended: 3-5 years for optimal rotation benefits',
            'start_year': 'Year when this rotation plan begins',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_year = cleaned_data.get('start_year')
        duration_years = cleaned_data.get('duration_years')
        
        if start_year and duration_years:
            end_year = start_year + duration_years - 1
            if end_year > 2100:
                raise forms.ValidationError(
                    f'End year ({end_year}) exceeds maximum allowed year (2100)'
                )
        
        return cleaned_data


class RotationSequenceForm(forms.ModelForm):
    """Form for adding/editing individual crops in a rotation sequence"""
    
    class Meta:
        model = RotationSequence
        fields = [
            'rotation_plan',
            'year_in_rotation',
            'crop_name',
            'variety',
            'planting_season',
            'expected_planting_month',
            'expected_harvest_month',
            'expected_yield_kg_per_acre',
            'nitrogen_requirement',
            'fertilizer_plan',
            'irrigation_plan',
            'pest_management_plan',
            'reason_for_selection',
        ]
        widgets = {
            'rotation_plan': forms.Select(attrs={
                'class': 'form-control',
            }),
            'year_in_rotation': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
            }),
            'crop_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Corn, Soybeans, Wheat',
                'list': 'crop-suggestions',
            }),
            'variety': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional: specific variety or cultivar',
            }),
            'planting_season': forms.Select(attrs={
                'class': 'form-control',
            }),
            'expected_planting_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 12,
            }),
            'expected_harvest_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 12,
            }),
            'expected_yield_kg_per_acre': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Expected yield in kg/acre',
            }),
            'nitrogen_requirement': forms.Select(attrs={
                'class': 'form-control',
            }),
            'fertilizer_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe fertilization strategy...',
            }),
            'irrigation_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe irrigation strategy...',
            }),
            'pest_management_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe pest and disease management...',
            }),
            'reason_for_selection': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why was this crop chosen for this year?',
            }),
        }
        help_texts = {
            'year_in_rotation': 'Position in the rotation cycle (1, 2, 3, etc.)',
            'expected_planting_month': 'Month number (1=January, 12=December)',
            'expected_harvest_month': 'Month number (1=January, 12=December)',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        planting_month = cleaned_data.get('expected_planting_month')
        harvest_month = cleaned_data.get('expected_harvest_month')
        
        # Note: We allow harvest < planting because crops can span calendar year
        # (e.g., plant in Oct, harvest in June)
        
        year_in_rotation = cleaned_data.get('year_in_rotation')
        rotation_plan = cleaned_data.get('rotation_plan')
        
        if year_in_rotation and rotation_plan:
            if year_in_rotation > rotation_plan.duration_years:
                raise forms.ValidationError(
                    f'Year {year_in_rotation} exceeds rotation duration ({rotation_plan.duration_years} years)'
                )
        
        return cleaned_data


class RotationBenefitForm(forms.ModelForm):
    """Form for documenting rotation benefits"""
    
    class Meta:
        model = RotationBenefit
        fields = [
            'rotation_plan',
            'benefit_type',
            'description',
            'expected_improvement_percent',
            'actual_improvement_percent',
            'expected_to_manifest_year',
            'priority',
            'is_verified',
            'verification_notes',
        ]
        widgets = {
            'rotation_plan': forms.Select(attrs={
                'class': 'form-control',
            }),
            'benefit_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the expected benefit in detail...',
            }),
            'expected_improvement_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '500',
                'placeholder': 'e.g., 15.5 for 15.5% improvement',
            }),
            'actual_improvement_percent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '-100',
                'max': '500',
                'placeholder': 'Actual improvement (leave blank if not yet verified)',
            }),
            'expected_to_manifest_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
            }),
            'priority': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'value': 5,
            }),
            'is_verified': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'verification_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notes on how this benefit was verified...',
            }),
        }
        help_texts = {
            'expected_to_manifest_year': 'Year in rotation when benefit is expected (1, 2, 3, etc.)',
            'priority': '1 = Low priority, 10 = High priority',
            'expected_improvement_percent': 'Can exceed 100% (e.g., 200% = tripling)',
        }


class GenerateRotationForm(forms.Form):
    """Form for generating AI rotation recommendations"""
    
    field = forms.ModelChoiceField(
        queryset=None,  # Set in __init__
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        help_text='Select the field for rotation planning'
    )
    
    duration_years = forms.IntegerField(
        min_value=2,
        max_value=10,
        initial=4,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        help_text='Length of rotation cycle (2-10 years, recommended: 3-5)'
    )
    
    start_year = forms.IntegerField(
        min_value=2000,
        max_value=2100,
        initial=datetime.now().year,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
        help_text='Year to start the rotation'
    )
    
    primary_goal = forms.ChoiceField(
        choices=RotationPlan._meta.get_field('primary_goal').choices,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        help_text='Primary objective of this rotation plan'
    )
    
    def __init__(self, *args, **kwargs):
        from fields.models import Field
        super().__init__(*args, **kwargs)
        self.fields['field'].queryset = Field.objects.all().order_by('name')
