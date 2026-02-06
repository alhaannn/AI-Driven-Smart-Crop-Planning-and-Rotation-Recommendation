from django.contrib import admin
from .models import FinancialRecord, PerformanceMetric, YieldForecast, Report


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'transaction_type',
        'category',
        'amount',
        'field',
        'crop_history',
        'vendor_buyer',
        'get_impact_display'
    ]
    
    list_filter = [
        'transaction_type',
        'category',
        'date',
        'payment_method',
        'is_recurring'
    ]
    
    search_fields = [
        'description',
        'vendor_buyer',
        'invoice_number',
        'notes'
    ]
    
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('transaction_type', 'category', 'amount', 'date')
        }),
        ('Related Entities', {
            'fields': ('field', 'crop_history')
        }),
        ('Transaction Details', {
            'fields': ('description', 'quantity', 'unit', 'vendor_buyer', 'invoice_number')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'is_recurring')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_impact_display(self, obj):
        impact = obj.get_impact()
        if impact > 0:
            return f"+${impact}"
        else:
            return f"${impact}"
    get_impact_display.short_description = 'Net Impact'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('field', 'crop_history')


@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = [
        'field',
        'metric_type',
        'score',
        'get_performance_level',
        'measurement_date',
        'year',
        'month'
    ]
    
    list_filter = [
        'metric_type',
        'year',
        'month',
        'measurement_date'
    ]
    
    search_fields = [
        'field__name',
        'notes'
    ]
    
    date_hierarchy = 'measurement_date'
    
    readonly_fields = ['get_performance_level', 'get_trend_color']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('field', 'metric_type', 'score')
        }),
        ('Time Period', {
            'fields': ('measurement_date', 'year', 'month')
        }),
        ('Calculation Details', {
            'fields': ('calculation_details', 'notes'),
            'classes': ('collapse',)
        }),
        ('Analysis', {
            'fields': ('get_performance_level', 'get_trend_color'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('field')


@admin.register(YieldForecast)
class YieldForecastAdmin(admin.ModelAdmin):
    list_display = [
        'field',
        'crop_name',
        'forecast_year',
        'planting_season',
        'predicted_yield_kg',
        'actual_yield_kg',
        'variance_percent',
        'confidence_level',
        'get_accuracy_status'
    ]
    
    list_filter = [
        'forecast_year',
        'planting_season',
        'prediction_method',
        'confidence_level'
    ]
    
    search_fields = [
        'field__name',
        'crop_name',
        'notes'
    ]
    
    readonly_fields = [
        'variance_percent',
        'get_accuracy_status',
        'get_predicted_yield_per_acre',
        'get_actual_yield_per_acre'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('field', 'crop_name', 'forecast_year', 'planting_season')
        }),
        ('Prediction', {
            'fields': (
                'predicted_yield_kg',
                'get_predicted_yield_per_acre',
                'confidence_level',
                'prediction_method',
                'factors_considered'
            )
        }),
        ('Actual Results', {
            'fields': (
                'actual_yield_kg',
                'get_actual_yield_per_acre',
                'variance_percent',
                'get_accuracy_status'
            ),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('field')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'report_type',
        'get_date_range',
        'is_published',
        'created_at',
        'generated_by'
    ]
    
    list_filter = [
        'report_type',
        'is_published',
        'created_at',
        'start_date',
        'end_date'
    ]
    
    search_fields = [
        'title',
        'description',
        'summary',
        'generated_by'
    ]
    
    date_hierarchy = 'created_at'
    
    filter_horizontal = ['fields_included']
    
    readonly_fields = ['get_date_range', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('report_type', 'title', 'description', 'generated_by')
        }),
        ('Time Period', {
            'fields': ('start_date', 'end_date', 'get_date_range')
        }),
        ('Content', {
            'fields': ('fields_included', 'report_data', 'summary')
        }),
        ('Publishing', {
            'fields': ('is_published', 'file_path')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
