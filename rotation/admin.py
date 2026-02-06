from django.contrib import admin
from .models import RotationPlan, RotationSequence, RotationBenefit


@admin.register(RotationPlan)
class RotationPlanAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'field',
        'start_year',
        'duration_years',
        'status',
        'primary_goal',
        'ai_generated',
        'confidence_score',
        'created_at',
    ]
    list_filter = [
        'status',
        'primary_goal',
        'ai_generated',
        'start_year',
        'created_at',
    ]
    search_fields = ['name', 'description', 'field__name', 'created_by']
    readonly_fields = ['created_at', 'updated_at', 'get_end_year', 'get_total_sequences']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('field', 'name', 'description', 'created_by')
        }),
        ('Timeline', {
            'fields': ('start_year', 'duration_years', 'get_end_year', 'status')
        }),
        ('Goals and AI', {
            'fields': ('primary_goal', 'ai_generated', 'confidence_score')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'get_total_sequences'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'created_at'
    
    def get_end_year(self, obj):
        return obj.get_end_year()
    get_end_year.short_description = 'End Year'
    
    def get_total_sequences(self, obj):
        return obj.get_total_sequences()
    get_total_sequences.short_description = 'Number of Sequences'


@admin.register(RotationSequence)
class RotationSequenceAdmin(admin.ModelAdmin):
    list_display = [
        'rotation_plan',
        'year_in_rotation',
        'crop_name',
        'variety',
        'planting_season',
        'nitrogen_requirement',
        'is_completed',
        'get_actual_year',
    ]
    list_filter = [
        'rotation_plan__field',
        'planting_season',
        'nitrogen_requirement',
        'is_completed',
        'year_in_rotation',
    ]
    search_fields = [
        'crop_name',
        'variety',
        'rotation_plan__name',
        'reason_for_selection',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'get_actual_year',
        'get_planting_date_estimate',
        'get_harvest_date_estimate',
        'get_growing_period_months',
    ]
    
    fieldsets = (
        ('Rotation Details', {
            'fields': ('rotation_plan', 'year_in_rotation', 'get_actual_year')
        }),
        ('Crop Information', {
            'fields': ('crop_name', 'variety', 'planting_season', 'nitrogen_requirement')
        }),
        ('Timeline', {
            'fields': (
                'expected_planting_month',
                'expected_harvest_month',
                'get_planting_date_estimate',
                'get_harvest_date_estimate',
                'get_growing_period_months',
            )
        }),
        ('Agricultural Plans', {
            'fields': (
                'fertilizer_plan',
                'irrigation_plan',
                'pest_management_plan',
                'expected_yield_kg_per_acre',
            )
        }),
        ('AI Reasoning', {
            'fields': ('reason_for_selection',)
        }),
        ('Completion Tracking', {
            'fields': ('is_completed', 'actual_crop_history'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['rotation_plan', 'year_in_rotation']
    
    def get_actual_year(self, obj):
        return obj.get_actual_year()
    get_actual_year.short_description = 'Calendar Year'
    
    def get_planting_date_estimate(self, obj):
        try:
            return obj.get_planting_date_estimate().strftime('%B %Y')
        except:
            return 'N/A'
    get_planting_date_estimate.short_description = 'Est. Planting Date'
    
    def get_harvest_date_estimate(self, obj):
        try:
            return obj.get_harvest_date_estimate().strftime('%B %Y')
        except:
            return 'N/A'
    get_harvest_date_estimate.short_description = 'Est. Harvest Date'
    
    def get_growing_period_months(self, obj):
        try:
            return f"{obj.get_growing_period_months()} months"
        except:
            return 'N/A'
    get_growing_period_months.short_description = 'Growing Period'


@admin.register(RotationBenefit)
class RotationBenefitAdmin(admin.ModelAdmin):
    list_display = [
        'rotation_plan',
        'benefit_type',
        'expected_improvement_percent',
        'actual_improvement_percent',
        'expected_to_manifest_year',
        'priority',
        'is_verified',
        'get_benefit_status',
    ]
    list_filter = [
        'benefit_type',
        'is_verified',
        'priority',
        'expected_to_manifest_year',
        'rotation_plan__field',
    ]
    search_fields = [
        'description',
        'verification_notes',
        'rotation_plan__name',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'get_benefit_status',
        'get_improvement_comparison',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('rotation_plan', 'benefit_type', 'description', 'priority')
        }),
        ('Expected Benefits', {
            'fields': ('expected_improvement_percent', 'expected_to_manifest_year')
        }),
        ('Actual Results', {
            'fields': (
                'is_verified',
                'actual_improvement_percent',
                'verification_notes',
                'get_benefit_status',
                'get_improvement_comparison',
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'created_at'
    ordering = ['-priority', 'rotation_plan', 'expected_to_manifest_year']
    
    def get_benefit_status(self, obj):
        return obj.get_benefit_status()
    get_benefit_status.short_description = 'Status'
    
    def get_improvement_comparison(self, obj):
        comparison = obj.get_improvement_comparison()
        if comparison:
            return f"Difference: {comparison['difference']:.1f}% | Achievement: {comparison['percentage_of_expected']:.1f}%"
        return 'N/A'
    get_improvement_comparison.short_description = 'Expected vs Actual'
