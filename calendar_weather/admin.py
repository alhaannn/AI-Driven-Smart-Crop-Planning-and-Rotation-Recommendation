from django.contrib import admin
from .models import WeatherData, CropCalendar, CropRecommendation


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['field', 'date', 'condition', 'temperature_high', 'temperature_low', 'rainfall_mm', 'is_manual']
    list_filter = ['condition', 'date', 'field', 'is_manual']
    search_fields = ['field__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('field', 'date', 'condition')
        }),
        ('Temperature', {
            'fields': ('temperature_high', 'temperature_low')
        }),
        ('Precipitation & Wind', {
            'fields': ('rainfall_mm', 'humidity_percent', 'wind_speed_kmh')
        }),
        ('Notes', {
            'fields': ('notes', 'is_manual')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CropCalendar)
class CropCalendarAdmin(admin.ModelAdmin):
    list_display = ['crop_name', 'field', 'activity_type', 'scheduled_date', 'status', 'send_reminder']
    list_filter = ['activity_type', 'status', 'scheduled_date', 'field']
    search_fields = ['crop_name', 'variety', 'field__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'scheduled_date'
    
    fieldsets = (
        ('Crop Information', {
            'fields': ('field', 'crop_name', 'variety', 'activity_type')
        }),
        ('Scheduling', {
            'fields': ('scheduled_date', 'end_date', 'status', 'estimated_duration_days')
        }),
        ('Weather Requirements', {
            'fields': ('recommended_temperature_min', 'recommended_temperature_max'),
            'classes': ('collapse',)
        }),
        ('Reminders', {
            'fields': ('send_reminder', 'reminder_days_before')
        }),
        ('Details', {
            'fields': ('description', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
    list_display = ['recommended_crop', 'field', 'planting_season', 'confidence_score', 'created_at']
    list_filter = ['planting_season', 'confidence_score', 'field', 'created_at']
    search_fields = ['recommended_crop', 'recommended_variety', 'field__name', 'reasoning']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Recommendation', {
            'fields': ('field', 'recommended_crop', 'recommended_variety')
        }),
        ('Timing', {
            'fields': ('planting_season', 'ideal_planting_window_start', 'ideal_planting_window_end')
        }),
        ('Analysis', {
            'fields': ('confidence_score', 'reasoning', 'expected_yield_range')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
