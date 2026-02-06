from django.db import models
from django.utils import timezone
from fields.models import Field, CropHistory
from rotation.models import RotationPlan
from decimal import Decimal


class FinancialRecord(models.Model):
    """
    Track financial transactions related to farming operations
    """
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
        ('investment', 'Investment'),
    ]
    
    CATEGORY_CHOICES = [
        # Expense categories
        ('seeds', 'Seeds & Planting Material'),
        ('fertilizer', 'Fertilizer'),
        ('pesticides', 'Pesticides & Herbicides'),
        ('irrigation', 'Irrigation & Water'),
        ('labor', 'Labor Costs'),
        ('equipment', 'Equipment & Machinery'),
        ('fuel', 'Fuel & Energy'),
        ('maintenance', 'Maintenance & Repairs'),
        ('storage', 'Storage & Warehousing'),
        ('transportation', 'Transportation'),
        ('consulting', 'Consulting & Services'),
        ('insurance', 'Insurance'),
        ('taxes', 'Taxes & Fees'),
        ('other_expense', 'Other Expenses'),
        
        # Income categories
        ('crop_sales', 'Crop Sales'),
        ('subsidies', 'Government Subsidies'),
        ('grants', 'Grants'),
        ('other_income', 'Other Income'),
        
        # Investment categories
        ('land', 'Land Purchase'),
        ('infrastructure', 'Infrastructure'),
        ('equipment_purchase', 'Equipment Purchase'),
        ('other_investment', 'Other Investments'),
    ]
    
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='financial_records',
        null=True,
        blank=True,
        help_text="Field related to this transaction (optional)"
    )
    
    crop_history = models.ForeignKey(
        CropHistory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='financial_records',
        help_text="Specific crop harvest related to this transaction"
    )
    
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        help_text="Type of financial transaction"
    )
    
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        help_text="Transaction category"
    )
    
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Transaction amount in local currency"
    )
    
    date = models.DateField(
        default=timezone.now,
        help_text="Transaction date"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the transaction"
    )
    
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Quantity (kg, liters, units, etc.)"
    )
    
    unit = models.CharField(
        max_length=20,
        blank=True,
        help_text="Unit of measurement (kg, liters, bags, etc.)"
    )
    
    vendor_buyer = models.CharField(
        max_length=200,
        blank=True,
        help_text="Vendor (for expenses) or Buyer (for income)"
    )
    
    invoice_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Invoice or receipt number"
    )
    
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('cash', 'Cash'),
            ('bank_transfer', 'Bank Transfer'),
            ('check', 'Check'),
            ('credit_card', 'Credit Card'),
            ('mobile_payment', 'Mobile Payment'),
            ('other', 'Other'),
        ],
        help_text="Payment method used"
    )
    
    is_recurring = models.BooleanField(
        default=False,
        help_text="Is this a recurring transaction?"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Financial Record'
        verbose_name_plural = 'Financial Records'
    
    def __str__(self):
        return f"{self.get_transaction_type_display()}: {self.get_category_display()} - ${self.amount} ({self.date})"
    
    def get_impact(self):
        """Return positive for income, negative for expense/investment"""
        if self.transaction_type == 'income':
            return self.amount
        else:
            return -self.amount
    
    def get_unit_price(self):
        """Calculate unit price if quantity is available"""
        if self.quantity and self.quantity > 0:
            return self.amount / self.quantity
        return None


class PerformanceMetric(models.Model):
    """
    Track key performance indicators for fields and crops
    """
    METRIC_TYPES = [
        ('yield_efficiency', 'Yield Efficiency'),
        ('soil_health_score', 'Soil Health Score'),
        ('profitability', 'Profitability'),
        ('resource_efficiency', 'Resource Efficiency'),
        ('sustainability_score', 'Sustainability Score'),
        ('crop_diversity', 'Crop Diversity'),
        ('rotation_adherence', 'Rotation Plan Adherence'),
        ('weather_resilience', 'Weather Resilience'),
        ('pest_resistance', 'Pest Resistance'),
        ('nutrient_balance', 'Nutrient Balance'),
    ]
    
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='performance_metrics'
    )
    
    metric_type = models.CharField(
        max_length=30,
        choices=METRIC_TYPES,
        help_text="Type of performance metric"
    )
    
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Performance score (0-100)"
    )
    
    measurement_date = models.DateField(
        default=timezone.now,
        help_text="Date of measurement"
    )
    
    year = models.IntegerField(
        help_text="Year of measurement"
    )
    
    month = models.IntegerField(
        null=True,
        blank=True,
        help_text="Month of measurement (1-12)"
    )
    
    calculation_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON data with calculation breakdown"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about this metric"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-measurement_date', 'field']
        verbose_name = 'Performance Metric'
        verbose_name_plural = 'Performance Metrics'
        unique_together = ['field', 'metric_type', 'measurement_date']
    
    def __str__(self):
        return f"{self.field.name} - {self.get_metric_type_display()}: {self.score}% ({self.measurement_date})"
    
    def get_performance_level(self):
        """Return performance level based on score"""
        if self.score >= 80:
            return 'Excellent'
        elif self.score >= 60:
            return 'Good'
        elif self.score >= 40:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def get_trend_color(self):
        """Return color for visualization based on score"""
        if self.score >= 80:
            return '#27ae60'  # Green
        elif self.score >= 60:
            return '#3498db'  # Blue
        elif self.score >= 40:
            return '#f39c12'  # Orange
        else:
            return '#e74c3c'  # Red


class YieldForecast(models.Model):
    """
    Store yield predictions and forecasts
    """
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='yield_forecasts'
    )
    
    crop_name = models.CharField(
        max_length=100,
        help_text="Crop being forecasted"
    )
    
    forecast_year = models.IntegerField(
        help_text="Year of the forecast"
    )
    
    planting_season = models.CharField(
        max_length=20,
        choices=[
            ('spring', 'Spring'),
            ('summer', 'Summer'),
            ('fall', 'Fall'),
            ('winter', 'Winter'),
        ],
        help_text="Planned planting season"
    )
    
    predicted_yield_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Predicted yield in kg"
    )
    
    confidence_level = models.IntegerField(
        default=70,
        help_text="Forecast confidence level (0-100%)"
    )
    
    prediction_method = models.CharField(
        max_length=50,
        choices=[
            ('historical_average', 'Historical Average'),
            ('trend_analysis', 'Trend Analysis'),
            ('ml_model', 'Machine Learning Model'),
            ('expert_estimate', 'Expert Estimate'),
            ('hybrid', 'Hybrid Method'),
        ],
        default='historical_average',
        help_text="Method used for prediction"
    )
    
    factors_considered = models.JSONField(
        default=dict,
        help_text="JSON data with factors considered in prediction"
    )
    
    actual_yield_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Actual yield achieved (filled after harvest)"
    )
    
    variance_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Variance between predicted and actual"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the forecast"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-forecast_year', 'field']
        verbose_name = 'Yield Forecast'
        verbose_name_plural = 'Yield Forecasts'
    
    def __str__(self):
        return f"{self.crop_name} @ {self.field.name} ({self.forecast_year}): {self.predicted_yield_kg} kg"
    
    def calculate_variance(self):
        """Calculate variance when actual yield is recorded"""
        if self.actual_yield_kg and self.predicted_yield_kg:
            variance = ((self.actual_yield_kg - self.predicted_yield_kg) / self.predicted_yield_kg) * 100
            self.variance_percent = round(variance, 2)
            return self.variance_percent
        return None
    
    def get_accuracy_status(self):
        """Return accuracy status based on variance"""
        if self.variance_percent is None:
            return 'Pending'
        
        abs_variance = abs(self.variance_percent)
        if abs_variance <= 10:
            return 'Excellent'
        elif abs_variance <= 20:
            return 'Good'
        elif abs_variance <= 30:
            return 'Fair'
        else:
            return 'Poor'
    
    def is_overestimated(self):
        """Check if prediction was overestimated"""
        if self.variance_percent:
            return self.variance_percent < 0
        return None
    
    def get_predicted_yield_per_acre(self):
        """Calculate predicted yield per acre"""
        if self.field.size_acres:
            return self.predicted_yield_kg / self.field.size_acres
        return None
    
    def get_actual_yield_per_acre(self):
        """Calculate actual yield per acre"""
        if self.actual_yield_kg and self.field.size_acres:
            return self.actual_yield_kg / self.field.size_acres
        return None


class Report(models.Model):
    """
    Store generated reports for future reference
    """
    REPORT_TYPES = [
        ('financial_summary', 'Financial Summary'),
        ('yield_analysis', 'Yield Analysis'),
        ('soil_health', 'Soil Health Report'),
        ('rotation_performance', 'Rotation Performance'),
        ('field_comparison', 'Field Comparison'),
        ('seasonal_overview', 'Seasonal Overview'),
        ('profitability', 'Profitability Analysis'),
        ('custom', 'Custom Report'),
    ]
    
    report_type = models.CharField(
        max_length=30,
        choices=REPORT_TYPES,
        help_text="Type of report"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Report title"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Report description"
    )
    
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text="Report period start date"
    )
    
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Report period end date"
    )
    
    fields_included = models.ManyToManyField(
        Field,
        blank=True,
        related_name='reports',
        help_text="Fields included in this report"
    )
    
    report_data = models.JSONField(
        default=dict,
        help_text="JSON data containing report metrics and data"
    )
    
    summary = models.TextField(
        blank=True,
        help_text="Executive summary of the report"
    )
    
    generated_by = models.CharField(
        max_length=100,
        blank=True,
        help_text="Person or system that generated the report"
    )
    
    file_path = models.CharField(
        max_length=500,
        blank=True,
        help_text="Path to exported PDF/CSV file"
    )
    
    is_published = models.BooleanField(
        default=False,
        help_text="Is this report published/finalized?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
    
    def __str__(self):
        return f"{self.get_report_type_display()}: {self.title} ({self.created_at.date()})"
    
    def get_date_range(self):
        """Return formatted date range"""
        if self.start_date and self.end_date:
            return f"{self.start_date} to {self.end_date}"
        return "Not specified"
