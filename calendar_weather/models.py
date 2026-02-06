from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta
from fields.models import Field, CropHistory


class WeatherData(models.Model):
    """
    Stores weather data for fields
    """
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='weather_data',
        help_text="Field where weather was recorded"
    )
    
    date = models.DateField(
        help_text="Date of weather observation"
    )
    
    # Temperature (Celsius)
    temperature_high = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(-50), MaxValueValidator(60)],
        help_text="High temperature in Celsius"
    )
    
    temperature_low = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(-50), MaxValueValidator(60)],
        help_text="Low temperature in Celsius"
    )
    
    # Precipitation
    rainfall_mm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        help_text="Rainfall in millimeters"
    )
    
    # Humidity
    humidity_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True,
        help_text="Relative humidity percentage"
    )
    
    # Wind
    wind_speed_kmh = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Wind speed in km/h"
    )
    
    # Conditions
    WEATHER_CONDITIONS = [
        ('sunny', 'Sunny'),
        ('partly_cloudy', 'Partly Cloudy'),
        ('cloudy', 'Cloudy'),
        ('rainy', 'Rainy'),
        ('stormy', 'Stormy'),
        ('foggy', 'Foggy'),
        ('snowy', 'Snowy'),
    ]
    
    condition = models.CharField(
        max_length=20,
        choices=WEATHER_CONDITIONS,
        default='sunny',
        help_text="General weather condition"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional weather observations"
    )
    
    # Data source
    is_manual = models.BooleanField(
        default=True,
        help_text="Whether data was manually entered or from API"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Weather Data'
        verbose_name_plural = 'Weather Data'
        unique_together = ['field', 'date']
    
    def __str__(self):
        return f"{self.field.name} - {self.date}: {self.get_condition_display()}"
    
    def get_avg_temperature(self):
        """Calculate average temperature"""
        return (float(self.temperature_high) + float(self.temperature_low)) / 2
    
    def is_favorable_for_planting(self):
        """Check if weather is suitable for planting"""
        avg_temp = self.get_avg_temperature()
        # General favorable conditions: 15-30°C, no heavy rain
        return 15 <= avg_temp <= 30 and float(self.rainfall_mm) < 50


class CropCalendar(models.Model):
    """
    Crop planting and harvesting calendar/schedule
    """
    ACTIVITY_TYPES = [
        ('planting', 'Planting'),
        ('irrigation', 'Irrigation'),
        ('fertilization', 'Fertilization'),
        ('pest_control', 'Pest Control'),
        ('harvesting', 'Harvesting'),
        ('soil_preparation', 'Soil Preparation'),
        ('pruning', 'Pruning'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('overdue', 'Overdue'),
    ]
    
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='calendar_events',
        help_text="Field for this activity"
    )
    
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPES,
        help_text="Type of farming activity"
    )
    
    crop_name = models.CharField(
        max_length=200,
        help_text="Crop name for this activity"
    )
    
    variety = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Crop variety (optional)"
    )
    
    scheduled_date = models.DateField(
        help_text="Scheduled date for activity"
    )
    
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="End date for multi-day activities (optional)"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        help_text="Current status of activity"
    )
    
    # Linked crop history (if activity resulted in harvest)
    crop_history = models.ForeignKey(
        CropHistory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='calendar_events',
        help_text="Linked crop history record"
    )
    
    # Activity details
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the activity"
    )
    
    estimated_duration_days = models.IntegerField(
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
        help_text="Estimated duration in days"
    )
    
    # Weather-based recommendations
    recommended_temperature_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Minimum recommended temperature (°C)"
    )
    
    recommended_temperature_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Maximum recommended temperature (°C)"
    )
    
    # Reminders
    send_reminder = models.BooleanField(
        default=True,
        help_text="Send reminder notification"
    )
    
    reminder_days_before = models.IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        help_text="Days before event to send reminder"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date']
        verbose_name = 'Crop Calendar Event'
        verbose_name_plural = 'Crop Calendar Events'
    
    def __str__(self):
        return f"{self.crop_name} - {self.get_activity_type_display()} on {self.scheduled_date}"
    
    def is_overdue(self):
        """Check if event is overdue"""
        if self.status in ['completed', 'cancelled']:
            return False
        return self.scheduled_date < timezone.now().date()
    
    def days_until(self):
        """Calculate days until scheduled date"""
        delta = self.scheduled_date - timezone.now().date()
        return delta.days
    
    def is_upcoming(self, days=7):
        """Check if event is upcoming within specified days"""
        days_left = self.days_until()
        return 0 <= days_left <= days
    
    def get_weather_suitability(self):
        """
        Check weather suitability based on forecast
        Returns: 'suitable', 'marginal', 'unsuitable', or 'no_data'
        """
        try:
            weather = WeatherData.objects.filter(
                field=self.field,
                date=self.scheduled_date
            ).first()
            
            if not weather:
                return 'no_data'
            
            avg_temp = weather.get_avg_temperature()
            
            # Check temperature range if specified
            if self.recommended_temperature_min and self.recommended_temperature_max:
                if self.recommended_temperature_min <= avg_temp <= self.recommended_temperature_max:
                    return 'suitable'
                elif abs(avg_temp - self.recommended_temperature_min) <= 5 or \
                     abs(avg_temp - self.recommended_temperature_max) <= 5:
                    return 'marginal'
                else:
                    return 'unsuitable'
            
            # Default favorable check
            if weather.is_favorable_for_planting():
                return 'suitable'
            else:
                return 'marginal'
                
        except Exception:
            return 'no_data'
    
    def save(self, *args, **kwargs):
        """Auto-update status to overdue if necessary"""
        if self.is_overdue() and self.status == 'planned':
            self.status = 'overdue'
        super().save(*args, **kwargs)


class CropRecommendation(models.Model):
    """
    AI-generated crop recommendations based on soil, weather, and history
    """
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='crop_recommendations',
        help_text="Field for recommendation"
    )
    
    recommended_crop = models.CharField(
        max_length=200,
        help_text="Recommended crop name"
    )
    
    recommended_variety = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Recommended variety"
    )
    
    planting_season = models.CharField(
        max_length=50,
        choices=[
            ('spring', 'Spring'),
            ('summer', 'Summer'),
            ('fall', 'Fall'),
            ('winter', 'Winter'),
            ('year_round', 'Year Round'),
        ],
        help_text="Best planting season"
    )
    
    confidence_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Confidence score (0-100)"
    )
    
    reasoning = models.TextField(
        help_text="Why this crop is recommended"
    )
    
    expected_yield_range = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Expected yield range (e.g., '2000-3000 kg/acre')"
    )
    
    ideal_planting_window_start = models.DateField(
        blank=True,
        null=True,
        help_text="Ideal planting window start"
    )
    
    ideal_planting_window_end = models.DateField(
        blank=True,
        null=True,
        help_text="Ideal planting window end"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-confidence_score', '-created_at']
        verbose_name = 'Crop Recommendation'
        verbose_name_plural = 'Crop Recommendations'
    
    def __str__(self):
        return f"{self.recommended_crop} for {self.field.name} ({self.confidence_score}% confidence)"
