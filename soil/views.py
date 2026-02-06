from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg
from .models import SoilAnalysis, NutrientRecommendation
from .forms import SoilAnalysisForm, NutrientRecommendationForm
from .utils import generate_recommendations, get_soil_health_score, get_health_rating
from fields.models import Field


# ============================================
# SOIL ANALYSIS VIEWS
# ============================================

def soil_analysis_list(request):
    """
    Display list of all soil analyses
    """
    soil_analyses = SoilAnalysis.objects.select_related('field').all()
    
    # Filter by field if specified
    field_id = request.GET.get('field')
    if field_id:
        soil_analyses = soil_analyses.filter(field_id=field_id)
    
    context = {
        'soil_analyses': soil_analyses,
        'fields': Field.objects.all(),
        'selected_field': field_id,
        'total_analyses': soil_analyses.count(),
    }
    return render(request, 'soil/soil_analysis_list.html', context)


def soil_analysis_detail(request, pk):
    """
    Display detailed soil analysis with nutrient visualizations
    """
    soil_analysis = get_object_or_404(SoilAnalysis, pk=pk)
    
    # Calculate health score
    health_score = get_soil_health_score(soil_analysis)
    health_rating = get_health_rating(health_score)
    
    # Get nutrient levels
    nutrient_levels = {
        'nitrogen': soil_analysis.get_nutrient_level('nitrogen', float(soil_analysis.nitrogen_ppm)),
        'phosphorus': soil_analysis.get_nutrient_level('phosphorus', float(soil_analysis.phosphorus_ppm)),
        'potassium': soil_analysis.get_nutrient_level('potassium', float(soil_analysis.potassium_ppm)),
    }
    
    # Get recommendations
    recommendations = soil_analysis.recommendations.all()
    
    context = {
        'soil_analysis': soil_analysis,
        'health_score': health_score,
        'health_rating': health_rating,
        'nutrient_levels': nutrient_levels,
        'recommendations': recommendations,
        'ph_status': soil_analysis.get_ph_status(),
        'om_status': soil_analysis.get_organic_matter_status(),
    }
    return render(request, 'soil/soil_analysis_detail.html', context)


def soil_analysis_create(request):
    """
    Create a new soil analysis
    """
    if request.method == 'POST':
        form = SoilAnalysisForm(request.POST)
        if form.is_valid():
            soil_analysis = form.save()
            
            # Generate automated recommendations
            recommendations = generate_recommendations(soil_analysis)
            
            messages.success(
                request,
                f'Soil analysis for {soil_analysis.field.name} created successfully! '
                f'{len(recommendations)} recommendations generated.'
            )
            return redirect('soil_analysis_detail', pk=soil_analysis.pk)
    else:
        # Pre-select field if provided
        field_id = request.GET.get('field')
        initial = {'field': field_id} if field_id else {}
        form = SoilAnalysisForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Add Soil Analysis',
        'button_text': 'Analyze Soil',
    }
    return render(request, 'soil/soil_analysis_form.html', context)


def soil_analysis_update(request, pk):
    """
    Update an existing soil analysis
    """
    soil_analysis = get_object_or_404(SoilAnalysis, pk=pk)
    
    if request.method == 'POST':
        form = SoilAnalysisForm(request.POST, instance=soil_analysis)
        if form.is_valid():
            soil_analysis = form.save()
            
            # Regenerate recommendations
            recommendations = generate_recommendations(soil_analysis)
            
            messages.success(
                request,
                f'Soil analysis updated successfully! '
                f'{len(recommendations)} recommendations regenerated.'
            )
            return redirect('soil_analysis_detail', pk=soil_analysis.pk)
    else:
        form = SoilAnalysisForm(instance=soil_analysis)
    
    context = {
        'form': form,
        'soil_analysis': soil_analysis,
        'title': f'Edit Soil Analysis - {soil_analysis.field.name}',
        'button_text': 'Update Analysis',
    }
    return render(request, 'soil/soil_analysis_form.html', context)


def soil_analysis_delete(request, pk):
    """
    Delete a soil analysis
    """
    soil_analysis = get_object_or_404(SoilAnalysis, pk=pk)
    
    if request.method == 'POST':
        field_name = soil_analysis.field.name
        soil_analysis.delete()
        messages.success(request, f'Soil analysis for {field_name} deleted successfully!')
        return redirect('soil_analysis_list')
    
    context = {
        'soil_analysis': soil_analysis,
    }
    return render(request, 'soil/soil_analysis_confirm_delete.html', context)


# ============================================
# NUTRIENT RECOMMENDATION VIEWS
# ============================================

def recommendation_list(request):
    """
    Display all nutrient recommendations
    """
    recommendations = NutrientRecommendation.objects.select_related('soil_analysis', 'soil_analysis__field').all()
    
    context = {
        'recommendations': recommendations,
    }
    return render(request, 'soil/recommendation_list.html', context)


def regenerate_recommendations(request, pk):
    """
    Regenerate recommendations for a soil analysis
    """
    soil_analysis = get_object_or_404(SoilAnalysis, pk=pk)
    
    recommendations = generate_recommendations(soil_analysis)
    
    messages.success(
        request,
        f'{len(recommendations)} recommendations regenerated for {soil_analysis.field.name}!'
    )
    return redirect('soil_analysis_detail', pk=soil_analysis.pk)


def nutrient_chart_data(request, pk):
    """
    API endpoint to provide data for nutrient charts
    """
    from django.http import JsonResponse
    
    soil_analysis = get_object_or_404(SoilAnalysis, pk=pk)
    
    data = {
        'labels': ['Nitrogen', 'Phosphorus', 'Potassium'],
        'values': [
            float(soil_analysis.nitrogen_ppm),
            float(soil_analysis.phosphorus_ppm),
            float(soil_analysis.potassium_ppm),
        ],
        'ph': float(soil_analysis.ph_level),
        'organic_matter': float(soil_analysis.organic_matter),
        'health_score': get_soil_health_score(soil_analysis),
    }
    
    return JsonResponse(data)
