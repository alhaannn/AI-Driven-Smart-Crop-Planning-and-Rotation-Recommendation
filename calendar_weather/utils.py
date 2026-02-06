"""
Utility functions for crop recommendations and calendar management
"""
from datetime import datetime, timedelta
from django.db.models import Avg
from .models import CropCalendar, CropRecommendation
from fields.models import Field, CropHistory
from soil.models import SoilAnalysis


def generate_crop_recommendations(field):
    """
    Generate AI-powered crop recommendations based on field history, soil, and season
    """
    recommendations = []
    
    # Clear existing recommendations for this field
    CropRecommendation.objects.filter(field=field).delete()
    
    # Get soil analysis
    soil_analysis = SoilAnalysis.objects.filter(field=field).order_by('-analysis_date').first()
    
    # Get crop history
    crop_histories = CropHistory.objects.filter(field=field).order_by('-harvest_date')[:5]
    
    # Get current month to determine season
    current_month = datetime.now().month
    
    # Define season
    if current_month in [3, 4, 5]:
        current_season = 'spring'
    elif current_month in [6, 7, 8]:
        current_season = 'summer'
    elif current_month in [9, 10, 11]:
        current_season = 'fall'
    else:
        current_season = 'winter'
    
    # Crop database with requirements
    crop_database = {
        'Wheat': {
            'seasons': ['fall', 'winter'],
            'ph_range': (6.0, 7.5),
            'nitrogen_min': 30,
            'yield_range': '2500-4000 kg/acre',
            'benefits': 'Cool season crop, good for rotation'
        },
        'Corn': {
            'seasons': ['spring', 'summer'],
            'ph_range': (5.8, 7.0),
            'nitrogen_min': 40,
            'yield_range': '3000-5000 kg/acre',
            'benefits': 'High yielding, nitrogen-demanding crop'
        },
        'Soybeans': {
            'seasons': ['spring', 'summer'],
            'ph_range': (6.0, 7.0),
            'nitrogen_min': 0,  # Nitrogen fixer
            'yield_range': '1500-3000 kg/acre',
            'benefits': 'Nitrogen-fixing legume, excellent for soil health'
        },
        'Rice': {
            'seasons': ['summer'],
            'ph_range': (5.5, 6.5),
            'nitrogen_min': 35,
            'yield_range': '3500-6000 kg/acre',
            'benefits': 'Water-intensive, high-yielding grain'
        },
        'Tomatoes': {
            'seasons': ['spring', 'summer'],
            'ph_range': (6.0, 6.8),
            'nitrogen_min': 25,
            'yield_range': '4000-8000 kg/acre',
            'benefits': 'High-value vegetable crop'
        },
        'Potatoes': {
            'seasons': ['spring', 'fall'],
            'ph_range': (5.0, 6.5),
            'nitrogen_min': 30,
            'yield_range': '8000-12000 kg/acre',
            'benefits': 'Hardy crop, good storage potential'
        },
        'Cotton': {
            'seasons': ['spring', 'summer'],
            'ph_range': (5.8, 8.0),
            'nitrogen_min': 35,
            'yield_range': '800-1500 kg/acre',
            'benefits': 'High-value fiber crop'
        },
        'Barley': {
            'seasons': ['fall', 'winter', 'spring'],
            'ph_range': (6.0, 7.0),
            'nitrogen_min': 25,
            'yield_range': '2000-3500 kg/acre',
            'benefits': 'Versatile grain crop, drought-tolerant'
        },
    }
    
    # Evaluate each crop
    for crop_name, crop_info in crop_database.items():
        confidence = 50  # Base confidence
        reasoning_parts = []
        
        # Season match
        if current_season in crop_info['seasons']:
            confidence += 20
            reasoning_parts.append(f"Ideal season for {crop_name} ({current_season})")
        else:
            confidence -= 10
            reasoning_parts.append(f"Not ideal season (better in {', '.join(crop_info['seasons'])})")
        
        # Soil pH check
        if soil_analysis:
            ph = float(soil_analysis.ph_level)
            ph_min, ph_max = crop_info['ph_range']
            
            if ph_min <= ph <= ph_max:
                confidence += 15
                reasoning_parts.append(f"pH level ({ph}) is optimal for {crop_name}")
            elif abs(ph - ph_min) <= 0.5 or abs(ph - ph_max) <= 0.5:
                confidence += 5
                reasoning_parts.append(f"pH level ({ph}) is acceptable")
            else:
                confidence -= 10
                reasoning_parts.append(f"pH level ({ph}) needs adjustment (optimal: {ph_min}-{ph_max})")
        
        # Nitrogen check
        if soil_analysis:
            nitrogen = float(soil_analysis.nitrogen_ppm)
            nitrogen_min = crop_info['nitrogen_min']
            
            if nitrogen >= nitrogen_min:
                confidence += 10
                reasoning_parts.append(f"Nitrogen levels ({nitrogen} ppm) are sufficient")
            else:
                confidence -= 5
                reasoning_parts.append(f"Nitrogen levels low ({nitrogen} ppm), supplementation recommended")
        
        # Rotation benefit (avoid same crop consecutively)
        if crop_histories.exists():
            last_crop = crop_histories.first().crop_name
            if last_crop.lower() == crop_name.lower():
                confidence -= 15
                reasoning_parts.append(f"Avoid planting same crop consecutively (last: {last_crop})")
            else:
                confidence += 10
                reasoning_parts.append(f"Good rotation from previous crop ({last_crop})")
        
        # Special case: Soybeans after heavy nitrogen users
        if crop_name == 'Soybeans' and crop_histories.exists():
            last_crop = crop_histories.first().crop_name
            if last_crop.lower() in ['corn', 'wheat', 'cotton']:
                confidence += 15
                reasoning_parts.append("Excellent as nitrogen-fixing crop after nitrogen-demanding crop")
        
        # Cap confidence
        confidence = max(min(confidence, 95), 10)
        
        # Calculate planting window
        if current_season in crop_info['seasons']:
            today = datetime.now().date()
            window_start = today
            window_end = today + timedelta(days=60)
        else:
            window_start = None
            window_end = None
        
        # Create recommendation
        recommendation = CropRecommendation.objects.create(
            field=field,
            recommended_crop=crop_name,
            planting_season=', '.join(crop_info['seasons']),
            confidence_score=confidence,
            reasoning='. '.join(reasoning_parts) + f". {crop_info['benefits']}.",
            expected_yield_range=crop_info['yield_range'],
            ideal_planting_window_start=window_start,
            ideal_planting_window_end=window_end
        )
        
        recommendations.append(recommendation)
    
    return recommendations


def get_upcoming_activities(field=None, days=30):
    """
    Get upcoming calendar activities
    """
    from django.utils import timezone
    today = timezone.now().date()
    end_date = today + timedelta(days=days)
    
    query = CropCalendar.objects.filter(
        scheduled_date__gte=today,
        scheduled_date__lte=end_date
    ).exclude(status__in=['completed', 'cancelled'])
    
    if field:
        query = query.filter(field=field)
    
    return query.order_by('scheduled_date')


def get_overdue_activities(field=None):
    """
    Get overdue calendar activities
    """
    from django.utils import timezone
    today = timezone.now().date()
    
    query = CropCalendar.objects.filter(
        scheduled_date__lt=today,
        status='planned'
    )
    
    if field:
        query = query.filter(field=field)
    
    return query.order_by('scheduled_date')


def create_calendar_from_recommendation(recommendation, scheduled_date=None):
    """
    Create calendar event from crop recommendation
    """
    if not scheduled_date:
        scheduled_date = recommendation.ideal_planting_window_start or datetime.now().date()
    
    calendar_event = CropCalendar.objects.create(
        field=recommendation.field,
        activity_type='planting',
        crop_name=recommendation.recommended_crop,
        variety=recommendation.recommended_variety,
        scheduled_date=scheduled_date,
        status='planned',
        description=f"Recommended planting based on: {recommendation.reasoning}",
        send_reminder=True,
        reminder_days_before=7,
        notes=f"Expected yield: {recommendation.expected_yield_range}"
    )
    
    return calendar_event
