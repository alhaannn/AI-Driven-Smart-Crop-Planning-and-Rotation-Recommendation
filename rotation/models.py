from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from fields.models import Field, CropHistory
from datetime import datetime, timedelta
from django.utils import timezone


class RotationPlan(models.Model):
    """
    Multi-year crop rotation plan for a field
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='rotation_plans')
    name = models.CharField(max_length=200, help_text="Name of this rotation plan")
    description = models.TextField(blank=True, help_text="Detailed description of rotation strategy")
    
    start_year = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    duration_years = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(10)],
        help_text="Number of years for this rotation cycle (2-10 years)"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Goals and objectives
    primary_goal = models.CharField(
        max_length=50,
        choices=[
            ('yield_max', 'Maximize Yield'),
            ('soil_health', 'Improve Soil Health'),
            ('pest_control', 'Pest and Disease Management'),
            ('profit_max', 'Maximize Profit'),
            ('sustainability', 'Long-term Sustainability'),
            ('organic', 'Organic Certification'),
        ],
        default='yield_max'
    )
    
    # AI recommendation data
    ai_generated = models.BooleanField(default=False, help_text="Was this plan AI-generated?")
    confidence_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=50,
        help_text="AI confidence in this rotation plan (0-100%)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, blank=True, help_text="User who created this plan")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rotation Plan'
        verbose_name_plural = 'Rotation Plans'
    
    def __str__(self):
        return f"{self.name} - {self.field.name} ({self.start_year}-{self.start_year + self.duration_years - 1})"
    
    def get_end_year(self):
        """Calculate the end year of the rotation"""
        return self.start_year + self.duration_years - 1
    
    def get_total_sequences(self):
        """Count total crop sequences in this plan"""
        return self.sequences.count()
    
    def is_active(self):
        """Check if this rotation plan is currently active"""
        current_year = datetime.now().year
        return (self.status == 'active' and 
                self.start_year <= current_year <= self.get_end_year())
    
    def get_current_year_sequence(self):
        """Get the crop sequence for the current year"""
        current_year = datetime.now().year
        if self.start_year <= current_year <= self.get_end_year():
            year_index = current_year - self.start_year
            try:
                return self.sequences.get(year_in_rotation=year_index + 1)
            except RotationSequence.DoesNotExist:
                return None
        return None
    
    def get_expected_benefits_summary(self):
        """Get summary of expected benefits"""
        benefits = self.benefits.all()
        return {
            'total_benefits': benefits.count(),
            'soil_health_improvement': benefits.filter(benefit_type='soil_health').count(),
            'pest_reduction': benefits.filter(benefit_type='pest_control').count(),
            'yield_increase': benefits.filter(benefit_type='yield_increase').count(),
        }


class RotationSequence(models.Model):
    """
    Individual crop in the rotation sequence (one crop per year)
    """
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('year_round', 'Year Round'),
    ]
    
    rotation_plan = models.ForeignKey(RotationPlan, on_delete=models.CASCADE, related_name='sequences')
    year_in_rotation = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Year number in the rotation cycle (1, 2, 3, etc.)"
    )
    
    crop_name = models.CharField(max_length=100, help_text="Name of the crop to plant")
    variety = models.CharField(max_length=100, blank=True, help_text="Specific variety/cultivar")
    
    planting_season = models.CharField(max_length=20, choices=SEASON_CHOICES, default='spring')
    expected_planting_month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Month number (1-12) for planting"
    )
    expected_harvest_month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Month number (1-12) for harvest"
    )
    
    # Agricultural details
    expected_yield_kg_per_acre = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Expected yield in kg per acre"
    )
    
    fertilizer_plan = models.TextField(blank=True, help_text="Fertilization strategy for this crop")
    irrigation_plan = models.TextField(blank=True, help_text="Irrigation strategy for this crop")
    pest_management_plan = models.TextField(blank=True, help_text="Pest and disease management")
    
    # Crop requirements
    nitrogen_requirement = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('nitrogen_fixing', 'Nitrogen Fixing')],
        default='medium'
    )
    
    # Rotation logic
    reason_for_selection = models.TextField(
        blank=True,
        help_text="Why this crop was chosen for this position in the rotation"
    )
    
    # Execution tracking
    is_completed = models.BooleanField(default=False, help_text="Has this sequence been completed?")
    actual_crop_history = models.ForeignKey(
        CropHistory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rotation_sequence',
        help_text="Link to actual crop history record when completed"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['rotation_plan', 'year_in_rotation']
        unique_together = ['rotation_plan', 'year_in_rotation']
        verbose_name = 'Rotation Sequence'
        verbose_name_plural = 'Rotation Sequences'
    
    def __str__(self):
        return f"Year {self.year_in_rotation}: {self.crop_name} ({self.rotation_plan.name})"
    
    def get_actual_year(self):
        """Calculate the actual calendar year for this sequence"""
        return self.rotation_plan.start_year + self.year_in_rotation - 1
    
    def is_nitrogen_fixer(self):
        """Check if this crop fixes nitrogen (e.g., legumes)"""
        return self.nitrogen_requirement == 'nitrogen_fixing'
    
    def get_planting_date_estimate(self):
        """Get estimated planting date for this sequence"""
        year = self.get_actual_year()
        return datetime(year, self.expected_planting_month, 1)
    
    def get_harvest_date_estimate(self):
        """Get estimated harvest date for this sequence"""
        year = self.get_actual_year()
        # Handle wrap-around to next year if harvest month < planting month
        if self.expected_harvest_month < self.expected_planting_month:
            year += 1
        return datetime(year, self.expected_harvest_month, 1)
    
    def get_growing_period_months(self):
        """Calculate growing period in months"""
        if self.expected_harvest_month >= self.expected_planting_month:
            return self.expected_harvest_month - self.expected_planting_month
        else:
            return 12 - self.expected_planting_month + self.expected_harvest_month


class RotationBenefit(models.Model):
    """
    Track expected and actual benefits from crop rotation
    """
    BENEFIT_TYPE_CHOICES = [
        ('soil_health', 'Soil Health Improvement'),
        ('pest_control', 'Pest and Disease Control'),
        ('yield_increase', 'Yield Increase'),
        ('nitrogen_fixation', 'Nitrogen Fixation'),
        ('organic_matter', 'Organic Matter Increase'),
        ('erosion_control', 'Erosion Control'),
        ('weed_suppression', 'Weed Suppression'),
        ('water_conservation', 'Water Conservation'),
        ('biodiversity', 'Biodiversity Enhancement'),
        ('profit_increase', 'Profit Increase'),
    ]
    
    rotation_plan = models.ForeignKey(RotationPlan, on_delete=models.CASCADE, related_name='benefits')
    benefit_type = models.CharField(max_length=50, choices=BENEFIT_TYPE_CHOICES)
    
    description = models.TextField(help_text="Detailed description of the expected benefit")
    
    # Quantification
    expected_improvement_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(500)],
        null=True,
        blank=True,
        help_text="Expected % improvement (e.g., 15.5 for 15.5% increase)"
    )
    
    actual_improvement_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(-100), MaxValueValidator(500)],
        null=True,
        blank=True,
        help_text="Actual % improvement achieved"
    )
    
    # Timeline
    expected_to_manifest_year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Year in rotation when benefit is expected to manifest"
    )
    
    is_verified = models.BooleanField(default=False, help_text="Has this benefit been verified?")
    verification_notes = models.TextField(blank=True, help_text="Notes on benefit verification")
    
    priority = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text="Priority of this benefit (1=low, 10=high)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'rotation_plan', 'expected_to_manifest_year']
        verbose_name = 'Rotation Benefit'
        verbose_name_plural = 'Rotation Benefits'
    
    def __str__(self):
        return f"{self.get_benefit_type_display()} - {self.rotation_plan.name}"
    
    def get_benefit_status(self):
        """Get status of benefit realization"""
        if self.is_verified:
            if self.actual_improvement_percent:
                if self.actual_improvement_percent >= (self.expected_improvement_percent or 0):
                    return "Exceeded Expectations"
                elif self.actual_improvement_percent >= (self.expected_improvement_percent or 0) * 0.7:
                    return "Met Expectations"
                else:
                    return "Below Expectations"
            return "Verified (No Data)"
        return "Not Yet Verified"
    
    def get_improvement_comparison(self):
        """Compare expected vs actual improvement"""
        if self.expected_improvement_percent and self.actual_improvement_percent:
            diff = self.actual_improvement_percent - self.expected_improvement_percent
            return {
                'difference': diff,
                'percentage_of_expected': (self.actual_improvement_percent / self.expected_improvement_percent) * 100
            }
        return None
