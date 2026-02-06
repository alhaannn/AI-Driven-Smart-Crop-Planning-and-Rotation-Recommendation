from django.contrib import admin
from .models import Field, CropHistory


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'size_acres', 'soil_type', 'irrigation_type', 'created_at']
    list_filter = ['soil_type', 'irrigation_type', 'created_at']
    search_fields = ['name', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'size_acres')
        }),
        ('Field Characteristics', {
            'fields': ('soil_type', 'irrigation_type', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CropHistory)
class CropHistoryAdmin(admin.ModelAdmin):
    list_display = ['crop_name', 'field', 'planting_date', 'harvest_date', 'yield_amount', 'created_at']
    list_filter = ['field', 'crop_name', 'planting_date', 'harvest_date']
    search_fields = ['crop_name', 'variety', 'field__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'harvest_date'
    
    fieldsets = (
        ('Crop Information', {
            'fields': ('field', 'crop_name', 'variety')
        }),
        ('Dates', {
            'fields': ('planting_date', 'harvest_date')
        }),
        ('Yield', {
            'fields': ('yield_amount',)
        }),
        ('Inputs', {
            'fields': ('fertilizer_used', 'pesticide_used')
        }),
        ('Additional Information', {
            'fields': ('weather_conditions', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
