from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from fields.models import Field


class SoilAnalysis(models.Model):
    """
    Stores soil analysis data for fields
    """
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='soil_analyses',
        help_text="Field where soil was analyzed"
    )
    
    analysis_date = models.DateField(
        help_text="Date when soil analysis was conducted"
    )
    
    # pH Level (0-14 scale)
    ph_level = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(14)],
        help_text="Soil pH level (0-14 scale)"
    )
    
    # Organic Matter percentage
    organic_matter = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Organic matter percentage"
    )
    
    # Macronutrients (in ppm - parts per million)
    nitrogen_ppm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Nitrogen content in ppm",
        verbose_name="Nitrogen (ppm)"
    )
    
    phosphorus_ppm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Phosphorus content in ppm",
        verbose_name="Phosphorus (ppm)"
    )
    
    potassium_ppm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Potassium content in ppm",
        verbose_name="Potassium (ppm)"
    )
    
    # Micronutrients (optional)
    calcium_ppm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Calcium content in ppm",
        verbose_name="Calcium (ppm)"
    )
    
    magnesium_ppm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Magnesium content in ppm",
        verbose_name="Magnesium (ppm)"
    )
    
    sulfur_ppm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Sulfur content in ppm",
        verbose_name="Sulfur (ppm)"
    )
    
    # Additional measurements
    cec = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
        help_text="Cation Exchange Capacity (meq/100g)",
        verbose_name="CEC"
    )
    
    moisture_content = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True,
        help_text="Soil moisture content percentage"
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional observations or lab notes"
    )
    
    lab_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name of the testing laboratory"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-analysis_date']
        verbose_name = 'Soil Analysis'
        verbose_name_plural = 'Soil Analyses'
    
    def __str__(self):
        return f"{self.field.name} - {self.analysis_date}"
    
    def get_ph_status(self):
        """Categorize pH level"""
        if self.ph_level < 5.5:
            return 'Acidic'
        elif self.ph_level <= 7.5:
            return 'Neutral'
        else:
            return 'Alkaline'
    
    def get_organic_matter_status(self):
        """Categorize organic matter content"""
        if self.organic_matter < 2.0:
            return 'Low'
        elif self.organic_matter <= 5.0:
            return 'Medium'
        else:
            return 'High'
    
    def get_nutrient_level(self, nutrient, value):
        """
        Determine nutrient level status (Low/Medium/High)
        Based on general agricultural standards
        """
        thresholds = {
            'nitrogen': {'low': 20, 'medium': 40},
            'phosphorus': {'low': 15, 'medium': 30},
            'potassium': {'low': 100, 'medium': 200},
        }
        
        if nutrient.lower() in thresholds:
            if value < thresholds[nutrient.lower()]['low']:
                return 'Low'
            elif value <= thresholds[nutrient.lower()]['medium']:
                return 'Medium'
            else:
                return 'High'
        return 'Unknown'


class NutrientRecommendation(models.Model):
    """
    Automated nutrient recommendations based on soil analysis
    """
    NUTRIENT_CHOICES = [
        ('nitrogen', 'Nitrogen'),
        ('phosphorus', 'Phosphorus'),
        ('potassium', 'Potassium'),
        ('calcium', 'Calcium'),
        ('magnesium', 'Magnesium'),
        ('sulfur', 'Sulfur'),
        ('ph', 'pH Adjustment'),
        ('organic_matter', 'Organic Matter'),
    ]
    
    LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('optimal', 'Optimal'),
    ]
    
    soil_analysis = models.ForeignKey(
        SoilAnalysis,
        on_delete=models.CASCADE,
        related_name='recommendations',
        help_text="Related soil analysis"
    )
    
    nutrient = models.CharField(
        max_length=50,
        choices=NUTRIENT_CHOICES,
        help_text="Nutrient or soil parameter"
    )
    
    current_level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        help_text="Current level status"
    )
    
    recommended_action = models.TextField(
        help_text="Recommended action to improve soil health"
    )
    
    application_rate = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Recommended application rate (e.g., '50 kg/acre')"
    )
    
    priority = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Priority level (1=Low, 10=High)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', 'nutrient']
        verbose_name = 'Nutrient Recommendation'
        verbose_name_plural = 'Nutrient Recommendations'
    
    def __str__(self):
        return f"{self.get_nutrient_display()} - {self.current_level} ({self.soil_analysis.field.name})"
