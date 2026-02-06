from django.contrib import admin
from .models import SoilAnalysis, NutrientRecommendation


@admin.register(SoilAnalysis)
class SoilAnalysisAdmin(admin.ModelAdmin):
    list_display = ['field', 'analysis_date', 'ph_level', 'organic_matter', 'nitrogen_ppm', 'phosphorus_ppm', 'potassium_ppm', 'lab_name']
    list_filter = ['analysis_date', 'field', 'lab_name']
    search_fields = ['field__name', 'lab_name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'analysis_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('field', 'analysis_date', 'lab_name')
        }),
        ('pH and Organic Matter', {
            'fields': ('ph_level', 'organic_matter')
        }),
        ('Macronutrients (N-P-K)', {
            'fields': ('nitrogen_ppm', 'phosphorus_ppm', 'potassium_ppm')
        }),
        ('Micronutrients', {
            'fields': ('calcium_ppm', 'magnesium_ppm', 'sulfur_ppm'),
            'classes': ('collapse',)
        }),
        ('Additional Measurements', {
            'fields': ('cec', 'moisture_content'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NutrientRecommendation)
class NutrientRecommendationAdmin(admin.ModelAdmin):
    list_display = ['soil_analysis', 'nutrient', 'current_level', 'priority', 'application_rate', 'created_at']
    list_filter = ['nutrient', 'current_level', 'priority', 'created_at']
    search_fields = ['soil_analysis__field__name', 'recommended_action']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Recommendation Details', {
            'fields': ('soil_analysis', 'nutrient', 'current_level', 'priority')
        }),
        ('Action', {
            'fields': ('recommended_action', 'application_rate')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
