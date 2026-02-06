from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import WeatherData, CropCalendar, CropRecommendation
from .forms import WeatherDataForm, CropCalendarForm, CropRecommendationForm
from .utils import (
    generate_crop_recommendations,
    get_upcoming_activities,
    get_overdue_activities,
    create_calendar_from_recommendation
)
from fields.models import Field


# ============================================
# WEATHER DATA VIEWS
# ============================================

def weather_list(request):
    """
    List all weather data
    """
    weather_data = WeatherData.objects.select_related('field').all()
    
    # Filter by field if specified
    field_id = request.GET.get('field')
    if field_id:
        weather_data = weather_data.filter(field_id=field_id)
    
    # Recent weather summary
    recent_weather = weather_data[:10]
    
    context = {
        'weather_data': recent_weather,
        'fields': Field.objects.all(),
        'selected_field': field_id,
        'total_records': weather_data.count(),
    }
    return render(request, 'calendar_weather/weather_list.html', context)


def weather_detail(request, pk):
    """
    Display detailed weather information
    """
    weather = get_object_or_404(WeatherData, pk=pk)
    
    context = {
        'weather': weather,
        'avg_temp': weather.get_avg_temperature(),
        'is_favorable': weather.is_favorable_for_planting(),
    }
    return render(request, 'calendar_weather/weather_detail.html', context)


def weather_create(request):
    """
    Create new weather record
    """
    if request.method == 'POST':
        form = WeatherDataForm(request.POST)
        if form.is_valid():
            weather = form.save()
            messages.success(request, f'Weather data for {weather.field.name} added successfully!')
            return redirect('weather_detail', pk=weather.pk)
    else:
        field_id = request.GET.get('field')
        initial = {'field': field_id, 'date': timezone.now().date()} if field_id else {'date': timezone.now().date()}
        form = WeatherDataForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Add Weather Data',
        'button_text': 'Save Weather Data',
    }
    return render(request, 'calendar_weather/weather_form.html', context)


def weather_update(request, pk):
    """
    Update weather record
    """
    weather = get_object_or_404(WeatherData, pk=pk)
    
    if request.method == 'POST':
        form = WeatherDataForm(request.POST, instance=weather)
        if form.is_valid():
            weather = form.save()
            messages.success(request, 'Weather data updated successfully!')
            return redirect('weather_detail', pk=weather.pk)
    else:
        form = WeatherDataForm(instance=weather)
    
    context = {
        'form': form,
        'weather': weather,
        'title': f'Edit Weather Data - {weather.field.name}',
        'button_text': 'Update Weather Data',
    }
    return render(request, 'calendar_weather/weather_form.html', context)


def weather_delete(request, pk):
    """
    Delete weather record
    """
    weather = get_object_or_404(WeatherData, pk=pk)
    
    if request.method == 'POST':
        field_name = weather.field.name
        date = weather.date
        weather.delete()
        messages.success(request, f'Weather data for {field_name} on {date} deleted successfully!')
        return redirect('weather_list')
    
    context = {
        'weather': weather,
    }
    return render(request, 'calendar_weather/weather_confirm_delete.html', context)


# ============================================
# CROP CALENDAR VIEWS
# ============================================

def calendar_view(request):
    """
    Main calendar view with upcoming and overdue activities
    """
    # Get filter parameters
    field_id = request.GET.get('field')
    activity_type = request.GET.get('activity_type')
    
    # Base query
    activities = CropCalendar.objects.select_related('field').all()
    
    if field_id:
        activities = activities.filter(field_id=field_id)
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    # Categorize activities
    today = timezone.now().date()
    
    upcoming = activities.filter(
        scheduled_date__gte=today,
        scheduled_date__lte=today + timedelta(days=30)
    ).exclude(status__in=['completed', 'cancelled']).order_by('scheduled_date')
    
    overdue = activities.filter(
        scheduled_date__lt=today
    ).exclude(status__in=['completed', 'cancelled']).order_by('scheduled_date')
    
    completed = activities.filter(status='completed').order_by('-scheduled_date')[:10]
    
    context = {
        'upcoming_activities': upcoming,
        'overdue_activities': overdue,
        'completed_activities': completed,
        'fields': Field.objects.all(),
        'selected_field': field_id,
        'selected_activity_type': activity_type,
        'activity_types': CropCalendar.ACTIVITY_TYPES,
    }
    return render(request, 'calendar_weather/calendar_view.html', context)


def calendar_detail(request, pk):
    """
    Display calendar event details
    """
    event = get_object_or_404(CropCalendar, pk=pk)
    
    # Get weather suitability
    weather_suitability = event.get_weather_suitability()
    
    # Get weather data for the scheduled date
    weather = WeatherData.objects.filter(
        field=event.field,
        date=event.scheduled_date
    ).first()
    
    context = {
        'event': event,
        'days_until': event.days_until(),
        'is_overdue': event.is_overdue(),
        'weather_suitability': weather_suitability,
        'weather': weather,
    }
    return render(request, 'calendar_weather/calendar_detail.html', context)


def calendar_create(request):
    """
    Create new calendar event
    """
    if request.method == 'POST':
        form = CropCalendarForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'{event.get_activity_type_display()} scheduled for {event.crop_name}!')
            return redirect('calendar_detail', pk=event.pk)
    else:
        field_id = request.GET.get('field')
        initial = {'field': field_id} if field_id else {}
        form = CropCalendarForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Schedule Activity',
        'button_text': 'Schedule',
    }
    return render(request, 'calendar_weather/calendar_form.html', context)


def calendar_update(request, pk):
    """
    Update calendar event
    """
    event = get_object_or_404(CropCalendar, pk=pk)
    
    if request.method == 'POST':
        form = CropCalendarForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Calendar event updated successfully!')
            return redirect('calendar_detail', pk=event.pk)
    else:
        form = CropCalendarForm(instance=event)
    
    context = {
        'form': form,
        'event': event,
        'title': f'Edit Event - {event.crop_name}',
        'button_text': 'Update Event',
    }
    return render(request, 'calendar_weather/calendar_form.html', context)


def calendar_delete(request, pk):
    """
    Delete calendar event
    """
    event = get_object_or_404(CropCalendar, pk=pk)
    
    if request.method == 'POST':
        crop_name = event.crop_name
        event.delete()
        messages.success(request, f'Calendar event for {crop_name} deleted successfully!')
        return redirect('calendar_view')
    
    context = {
        'event': event,
    }
    return render(request, 'calendar_weather/calendar_confirm_delete.html', context)


def mark_complete(request, pk):
    """
    Mark calendar event as complete
    """
    event = get_object_or_404(CropCalendar, pk=pk)
    event.status = 'completed'
    event.save()
    messages.success(request, f'{event.crop_name} - {event.get_activity_type_display()} marked as complete!')
    return redirect('calendar_view')


# ============================================
# CROP RECOMMENDATION VIEWS
# ============================================

def recommendations_view(request, field_id=None):
    """
    View crop recommendations
    """
    if field_id:
        field = get_object_or_404(Field, pk=field_id)
        recommendations = CropRecommendation.objects.filter(field=field)
    else:
        field = None
        recommendations = CropRecommendation.objects.all()
    
    context = {
        'recommendations': recommendations,
        'field': field,
        'fields': Field.objects.all(),
    }
    return render(request, 'calendar_weather/recommendations_view.html', context)


def generate_recommendations_view(request, field_id):
    """
    Generate crop recommendations for a field
    """
    field = get_object_or_404(Field, pk=field_id)
    
    recommendations = generate_crop_recommendations(field)
    
    messages.success(
        request,
        f'{len(recommendations)} crop recommendations generated for {field.name}!'
    )
    return redirect('recommendations_view', field_id=field.pk)


def schedule_from_recommendation(request, rec_id):
    """
    Create calendar event from recommendation
    """
    recommendation = get_object_or_404(CropRecommendation, pk=rec_id)
    
    event = create_calendar_from_recommendation(recommendation)
    
    messages.success(
        request,
        f'Planting scheduled for {recommendation.recommended_crop} on {event.scheduled_date}!'
    )
    return redirect('calendar_detail', pk=event.pk)
