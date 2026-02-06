"""
Utility functions for soil analysis and nutrient recommendations
"""
from .models import NutrientRecommendation


def generate_recommendations(soil_analysis):
    """
    Generate automated nutrient recommendations based on soil analysis data
    Returns list of created NutrientRecommendation objects
    """
    recommendations = []
    
    # Clear existing recommendations for this analysis
    soil_analysis.recommendations.all().delete()
    
    # pH Recommendations
    ph_status = soil_analysis.get_ph_status()
    if ph_status == 'Acidic':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='ph',
            current_level='low',
            recommended_action='Apply lime (calcium carbonate) to raise pH to optimal range (6.0-7.0). This will improve nutrient availability.',
            application_rate='1-2 tons/acre',
            priority=9
        ))
    elif ph_status == 'Alkaline':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='ph',
            current_level='high',
            recommended_action='Apply sulfur or acidifying fertilizers to lower pH. Consider gypsum for alkaline soils.',
            application_rate='100-200 lbs/acre',
            priority=8
        ))
    
    # Organic Matter Recommendations
    om_status = soil_analysis.get_organic_matter_status()
    if om_status == 'Low':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='organic_matter',
            current_level='low',
            recommended_action='Increase organic matter through compost application, cover crops, or green manure. This improves soil structure and water retention.',
            application_rate='2-4 tons compost/acre',
            priority=7
        ))
    
    # Nitrogen Recommendations
    n_level = soil_analysis.get_nutrient_level('nitrogen', float(soil_analysis.nitrogen_ppm))
    if n_level == 'Low':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='nitrogen',
            current_level='low',
            recommended_action='Apply nitrogen fertilizer. Consider urea (46-0-0) or ammonium nitrate (34-0-0). Plant legume cover crops for organic nitrogen.',
            application_rate='80-120 lbs N/acre',
            priority=10
        ))
    elif n_level == 'High':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='nitrogen',
            current_level='high',
            recommended_action='Nitrogen levels are adequate. Avoid over-application to prevent leaching and environmental issues.',
            application_rate='Maintain current levels',
            priority=3
        ))
    
    # Phosphorus Recommendations
    p_level = soil_analysis.get_nutrient_level('phosphorus', float(soil_analysis.phosphorus_ppm))
    if p_level == 'Low':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='phosphorus',
            current_level='low',
            recommended_action='Apply phosphate fertilizer. Use DAP (18-46-0) or rock phosphate for organic systems. Essential for root development.',
            application_rate='60-100 lbs P2O5/acre',
            priority=9
        ))
    elif p_level == 'High':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='phosphorus',
            current_level='high',
            recommended_action='Phosphorus levels are sufficient. Reduce or eliminate phosphorus fertilization.',
            application_rate='No application needed',
            priority=2
        ))
    
    # Potassium Recommendations
    k_level = soil_analysis.get_nutrient_level('potassium', float(soil_analysis.potassium_ppm))
    if k_level == 'Low':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='potassium',
            current_level='low',
            recommended_action='Apply potassium fertilizer. Use potash (0-0-60) or wood ash. Important for disease resistance and water regulation.',
            application_rate='100-150 lbs K2O/acre',
            priority=8
        ))
    elif k_level == 'High':
        recommendations.append(NutrientRecommendation.objects.create(
            soil_analysis=soil_analysis,
            nutrient='potassium',
            current_level='high',
            recommended_action='Potassium levels are good. Maintain with balanced fertilization.',
            application_rate='Maintenance only',
            priority=2
        ))
    
    return recommendations


def get_soil_health_score(soil_analysis):
    """
    Calculate overall soil health score (0-100) based on multiple factors
    """
    score = 0
    max_score = 100
    
    # pH Score (20 points)
    ph = float(soil_analysis.ph_level)
    if 6.0 <= ph <= 7.0:
        score += 20
    elif 5.5 <= ph <= 7.5:
        score += 15
    elif 5.0 <= ph <= 8.0:
        score += 10
    else:
        score += 5
    
    # Organic Matter Score (20 points)
    om = float(soil_analysis.organic_matter)
    if om >= 5.0:
        score += 20
    elif om >= 3.0:
        score += 15
    elif om >= 2.0:
        score += 10
    else:
        score += 5
    
    # Nitrogen Score (20 points)
    n_level = soil_analysis.get_nutrient_level('nitrogen', float(soil_analysis.nitrogen_ppm))
    if n_level == 'High':
        score += 20
    elif n_level == 'Medium':
        score += 15
    else:
        score += 5
    
    # Phosphorus Score (20 points)
    p_level = soil_analysis.get_nutrient_level('phosphorus', float(soil_analysis.phosphorus_ppm))
    if p_level == 'High':
        score += 20
    elif p_level == 'Medium':
        score += 15
    else:
        score += 5
    
    # Potassium Score (20 points)
    k_level = soil_analysis.get_nutrient_level('potassium', float(soil_analysis.potassium_ppm))
    if k_level == 'High':
        score += 20
    elif k_level == 'Medium':
        score += 15
    else:
        score += 5
    
    return score


def get_health_rating(score):
    """
    Convert numeric score to health rating
    """
    if score >= 85:
        return 'Excellent'
    elif score >= 70:
        return 'Good'
    elif score >= 55:
        return 'Fair'
    elif score >= 40:
        return 'Poor'
    else:
        return 'Very Poor'
