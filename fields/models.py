from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Field(models.Model):
    """
    Represents a farm field with its characteristics
    """
    SOIL_TYPE_CHOICES = [
        ('clay', 'Clay'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('silty', 'Silty'),
        ('peaty', 'Peaty'),
        ('chalky', 'Chalky'),
    ]
    
    IRRIGATION_TYPE_CHOICES = [
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler'),
        ('flood', 'Flood/Surface'),
        ('furrow', 'Furrow'),
        ('rainfed', 'Rainfed'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Unique identifier for the field (e.g., 'North Field A')"
    )
    
    location = models.CharField(
        max_length=300,
        help_text="Geographic location or coordinates"
    )
    
    size_acres = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Field size in acres"
    )
    
    soil_type = models.CharField(
        max_length=50,
        choices=SOIL_TYPE_CHOICES,
        help_text="Primary soil classification"
    )
    
    irrigation_type = models.CharField(
        max_length=50,
        choices=IRRIGATION_TYPE_CHOICES,
        help_text="Irrigation method used"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the field"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Field'
        verbose_name_plural = 'Fields'
    
    def __str__(self):
        return f"{self.name} ({self.size_acres} acres)"
    
    def get_total_crop_history_count(self):
        """Returns the total number of crop history records for this field"""
        return self.crop_histories.count()
    
    def get_latest_crop(self):
        """Returns the most recent crop grown in this field"""
        latest = self.crop_histories.order_by('-harvest_date').first()
        return latest.crop_name if latest else "None"


class CropHistory(models.Model):
    """
    Records historical data about crops grown in fields
    """
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='crop_histories',
        help_text="Field where the crop was grown"
    )
    
    crop_name = models.CharField(
        max_length=200,
        help_text="Name of the crop (e.g., 'Wheat', 'Corn', 'Soybeans')"
    )
    
    variety = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Specific variety or cultivar"
    )
    
    planting_date = models.DateField(
        help_text="Date when the crop was planted"
    )
    
    harvest_date = models.DateField(
        help_text="Date when the crop was harvested"
    )
    
    yield_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Yield in kg per acre"
    )
    
    fertilizer_used = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Fertilizers applied during growth"
    )
    
    pesticide_used = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Pesticides or herbicides applied"
    )
    
    weather_conditions = models.TextField(
        blank=True,
        null=True,
        help_text="Notable weather conditions during growing season"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional observations or notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-harvest_date']
        verbose_name = 'Crop History'
        verbose_name_plural = 'Crop Histories'
    
    def __str__(self):
        return f"{self.crop_name} in {self.field.name} ({self.harvest_date.year})"
    
    def get_growing_days(self):
        """Calculate the number of days from planting to harvest"""
        if self.planting_date and self.harvest_date:
            delta = self.harvest_date - self.planting_date
            return delta.days
        return None
    
    def get_yield_per_field(self):
        """Calculate total yield for the entire field"""
        return self.yield_amount * self.field.size_acres
