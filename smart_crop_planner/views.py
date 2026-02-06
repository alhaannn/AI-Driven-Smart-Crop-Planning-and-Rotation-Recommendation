from django.shortcuts import render
from django.db.models import Count, Avg
from fields.models import Field, CropHistory
from soil.models import SoilAnalysis
from rotation.models import RotationPlan


def home_view(request):
    """
    Dashboard homepage view with real data
    """
    fields = Field.objects.all()
    crop_histories = CropHistory.objects.all()
    soil_analyses = SoilAnalysis.objects.all()
    rotation_plans = RotationPlan.objects.all()
    
    # Calculate statistics
    total_fields = fields.count()
    soil_analyses_count = soil_analyses.count()
    avg_yield = crop_histories.aggregate(Avg('yield_amount'))['yield_amount__avg'] or 0
    
    # Phase 5: Rotation plan statistics
    active_rotation_plans = rotation_plans.filter(status='active')
    active_plans_count = active_rotation_plans.count()
    
    # Get recent fields and rotation plans
    recent_fields = fields.order_by('-created_at')[:5]
    recent_rotation_plans = rotation_plans.order_by('-created_at')[:5]
    
    context = {
        'total_fields': total_fields,
        'active_plans': active_plans_count,
        'soil_analyses': soil_analyses_count,
        'avg_score': f"{avg_yield:.1f}" if avg_yield > 0 else 'N/A',
        'recent_fields': recent_fields,
        'active_rotation_plans': recent_rotation_plans,
    }
    return render(request, 'home.html', context)

