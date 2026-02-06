"""
Intelligent Crop Rotation Recommendation Engine
Generates AI-powered rotation plans based on field history, soil data, and weather patterns
"""

from datetime import datetime
from decimal import Decimal
from rotation.models import RotationPlan, RotationSequence, RotationBenefit


# Comprehensive crop database with rotation characteristics
CROP_DATABASE = {
    'Wheat': {
        'category': 'cereal',
        'nitrogen_requirement': 'high',
        'season': ['fall', 'winter'],
        'planting_month': 10,
        'harvest_month': 6,
        'ph_range': (6.0, 7.5),
        'expected_yield': (2500, 4000),
        'rotation_benefits': ['erosion_control', 'organic_matter'],
        'good_predecessors': ['Soybeans', 'Alfalfa', 'Clover'],
        'poor_predecessors': ['Wheat', 'Barley', 'Oats'],
        'good_successors': ['Soybeans', 'Corn', 'Potatoes'],
    },
    'Corn': {
        'category': 'cereal',
        'nitrogen_requirement': 'high',
        'season': ['spring', 'summer'],
        'planting_month': 4,
        'harvest_month': 9,
        'ph_range': (5.8, 7.0),
        'expected_yield': (4000, 8000),
        'rotation_benefits': ['yield_increase', 'weed_suppression'],
        'good_predecessors': ['Soybeans', 'Alfalfa', 'Clover'],
        'poor_predecessors': ['Corn', 'Sorghum'],
        'good_successors': ['Soybeans', 'Wheat', 'Alfalfa'],
    },
    'Soybeans': {
        'category': 'legume',
        'nitrogen_requirement': 'nitrogen_fixing',
        'season': ['spring', 'summer'],
        'planting_month': 5,
        'harvest_month': 10,
        'ph_range': (6.0, 7.0),
        'expected_yield': (1500, 3000),
        'rotation_benefits': ['nitrogen_fixation', 'soil_health', 'pest_control'],
        'good_predecessors': ['Corn', 'Wheat', 'Any non-legume'],
        'poor_predecessors': ['Soybeans', 'Other legumes'],
        'good_successors': ['Corn', 'Wheat', 'Any nitrogen-demanding crop'],
    },
    'Alfalfa': {
        'category': 'legume',
        'nitrogen_requirement': 'nitrogen_fixing',
        'season': ['spring', 'year_round'],
        'planting_month': 4,
        'harvest_month': 9,
        'ph_range': (6.5, 7.5),
        'expected_yield': (3000, 6000),
        'rotation_benefits': ['nitrogen_fixation', 'soil_health', 'organic_matter', 'erosion_control'],
        'good_predecessors': ['Corn', 'Wheat', 'Any cereal'],
        'poor_predecessors': ['Alfalfa', 'Clover'],
        'good_successors': ['Corn', 'Wheat', 'Cotton'],
        'multi_year': True,  # Can be grown for 3-5 years
    },
    'Potatoes': {
        'category': 'tuber',
        'nitrogen_requirement': 'medium',
        'season': ['spring', 'summer'],
        'planting_month': 4,
        'harvest_month': 8,
        'ph_range': (5.0, 6.5),
        'expected_yield': (8000, 15000),
        'rotation_benefits': ['weed_suppression', 'profit_increase'],
        'good_predecessors': ['Wheat', 'Oats', 'Legumes'],
        'poor_predecessors': ['Potatoes', 'Tomatoes', 'Peppers'],
        'good_successors': ['Legumes', 'Cereals'],
    },
    'Cotton': {
        'category': 'fiber',
        'nitrogen_requirement': 'high',
        'season': ['spring', 'summer'],
        'planting_month': 4,
        'harvest_month': 10,
        'ph_range': (5.8, 8.0),
        'expected_yield': (800, 1500),
        'rotation_benefits': ['profit_increase'],
        'good_predecessors': ['Alfalfa', 'Soybeans', 'Wheat'],
        'poor_predecessors': ['Cotton'],
        'good_successors': ['Wheat', 'Corn', 'Soybeans'],
    },
    'Tomatoes': {
        'category': 'vegetable',
        'nitrogen_requirement': 'medium',
        'season': ['spring', 'summer'],
        'planting_month': 4,
        'harvest_month': 8,
        'ph_range': (6.0, 7.0),
        'expected_yield': (20000, 40000),
        'rotation_benefits': ['profit_increase'],
        'good_predecessors': ['Legumes', 'Cereals'],
        'poor_predecessors': ['Tomatoes', 'Potatoes', 'Peppers'],
        'good_successors': ['Legumes', 'Cereals'],
    },
    'Rice': {
        'category': 'cereal',
        'nitrogen_requirement': 'high',
        'season': ['spring', 'summer'],
        'planting_month': 5,
        'harvest_month': 10,
        'ph_range': (5.5, 7.0),
        'expected_yield': (3000, 5000),
        'rotation_benefits': ['weed_suppression', 'water_conservation'],
        'good_predecessors': ['Legumes', 'Any crop'],
        'poor_predecessors': ['Rice'],
        'good_successors': ['Wheat', 'Legumes'],
    },
    'Barley': {
        'category': 'cereal',
        'nitrogen_requirement': 'medium',
        'season': ['fall', 'spring'],
        'planting_month': 10,
        'harvest_month': 6,
        'ph_range': (6.0, 7.0),
        'expected_yield': (2000, 3500),
        'rotation_benefits': ['erosion_control', 'weed_suppression'],
        'good_predecessors': ['Legumes', 'Corn'],
        'poor_predecessors': ['Barley', 'Wheat', 'Oats'],
        'good_successors': ['Legumes', 'Potatoes'],
    },
    'Clover': {
        'category': 'legume',
        'nitrogen_requirement': 'nitrogen_fixing',
        'season': ['spring', 'year_round'],
        'planting_month': 4,
        'harvest_month': 9,
        'ph_range': (6.0, 7.0),
        'expected_yield': (2000, 4000),
        'rotation_benefits': ['nitrogen_fixation', 'soil_health', 'erosion_control'],
        'good_predecessors': ['Cereals', 'Any crop'],
        'poor_predecessors': ['Legumes'],
        'good_successors': ['Corn', 'Wheat', 'Potatoes'],
        'multi_year': True,
    },
}


def generate_rotation_plan(field, duration_years=4, primary_goal='yield_max', start_year=None):
    """
    AI-powered crop rotation plan generator
    
    Args:
        field: Field object
        duration_years: Length of rotation cycle (2-10 years)
        primary_goal: Primary goal of rotation (yield_max, soil_health, etc.)
        start_year: Starting year (defaults to current year)
    
    Returns:
        Dictionary with rotation plan details
    """
    if start_year is None:
        start_year = datetime.now().year
    
    # Get field history and soil data
    crop_history = list(field.crop_histories.order_by('-harvest_date')[:5])
    recent_crops = [h.crop_name for h in crop_history]
    last_crop = recent_crops[0] if recent_crops else None
    
    # Get latest soil analysis
    soil_analysis = field.soil_analyses.order_by('-analysis_date').first()
    
    # Score each crop for the rotation
    crop_scores = {}
    for crop_name, crop_data in CROP_DATABASE.items():
        score = calculate_crop_rotation_score(
            crop_name,
            crop_data,
            field,
            last_crop,
            recent_crops,
            soil_analysis,
            primary_goal
        )
        crop_scores[crop_name] = score
    
    # Build rotation sequence
    rotation_sequence = []
    used_crops = []
    previous_crop = last_crop
    
    for year in range(1, duration_years + 1):
        # Get best crop for this position
        best_crop = select_best_crop(
            crop_scores,
            previous_crop,
            used_crops,
            year,
            duration_years,
            primary_goal
        )
        
        crop_info = CROP_DATABASE[best_crop]
        
        sequence_data = {
            'year': year,
            'crop': best_crop,
            'variety': '',
            'planting_season': crop_info['season'][0],
            'planting_month': crop_info['planting_month'],
            'harvest_month': crop_info['harvest_month'],
            'nitrogen_requirement': crop_info['nitrogen_requirement'],
            'expected_yield': crop_info['expected_yield'],
            'score': crop_scores[best_crop],
            'reasoning': generate_crop_reasoning(best_crop, crop_info, previous_crop, year, primary_goal),
        }
        
        rotation_sequence.append(sequence_data)
        used_crops.append(best_crop)
        previous_crop = best_crop
    
    # Calculate expected benefits
    benefits = calculate_rotation_benefits(rotation_sequence, primary_goal)
    
    # Calculate overall confidence score
    avg_score = sum(s['score'] for s in rotation_sequence) / len(rotation_sequence)
    confidence_score = min(95, max(60, int(avg_score)))
    
    return {
        'field': field,
        'duration_years': duration_years,
        'start_year': start_year,
        'primary_goal': primary_goal,
        'confidence_score': confidence_score,
        'sequences': rotation_sequence,
        'benefits': benefits,
        'summary': generate_rotation_summary(rotation_sequence, benefits, field),
    }


def calculate_crop_rotation_score(crop_name, crop_data, field, last_crop, recent_crops, soil_analysis, primary_goal):
    """
    Calculate suitability score for a crop in rotation (0-100)
    """
    score = 50  # Base score
    
    # Factor 1: Rotation compatibility (30 points)
    if last_crop:
        if last_crop in crop_data.get('good_predecessors', []):
            score += 20
        elif last_crop in crop_data.get('poor_predecessors', []):
            score -= 25
        
        # Avoid repeating same crop
        if crop_name == last_crop:
            score -= 30
        
        # Avoid repeating same category too frequently
        if last_crop in CROP_DATABASE:
            last_category = CROP_DATABASE[last_crop]['category']
            if crop_data['category'] == last_category and crop_data['category'] != 'legume':
                score -= 10
    
    # Factor 2: Diversification (15 points)
    if crop_name not in recent_crops[:3]:
        score += 15
    elif crop_name in recent_crops[:2]:
        score -= 15
    
    # Factor 3: Soil compatibility (20 points)
    if soil_analysis:
        ph = float(soil_analysis.ph_level)
        ph_min, ph_max = crop_data['ph_range']
        
        if ph_min <= ph <= ph_max:
            score += 15
        elif ph_min - 0.5 <= ph <= ph_max + 0.5:
            score += 8
        else:
            score -= 10
        
        # Nitrogen management
        nitrogen_ppm = float(soil_analysis.nitrogen_ppm)
        if crop_data['nitrogen_requirement'] == 'nitrogen_fixing':
            # Legumes are great after nitrogen-demanding crops
            if last_crop in ['Corn', 'Wheat', 'Cotton']:
                score += 15
        elif crop_data['nitrogen_requirement'] == 'high' and nitrogen_ppm < 30:
            score -= 10
        elif crop_data['nitrogen_requirement'] == 'low' and nitrogen_ppm > 50:
            score += 5
    
    # Factor 4: Goal alignment (20 points)
    if primary_goal == 'yield_max':
        avg_yield = sum(crop_data['expected_yield']) / 2
        if avg_yield > 5000:
            score += 15
        elif avg_yield > 3000:
            score += 10
    elif primary_goal == 'soil_health':
        if 'soil_health' in crop_data.get('rotation_benefits', []):
            score += 20
        if crop_data['nitrogen_requirement'] == 'nitrogen_fixing':
            score += 15
    elif primary_goal == 'pest_control':
        if 'pest_control' in crop_data.get('rotation_benefits', []):
            score += 20
    elif primary_goal == 'profit_max':
        if 'profit_increase' in crop_data.get('rotation_benefits', []):
            score += 15
        avg_yield = sum(crop_data['expected_yield']) / 2
        if avg_yield > 10000:
            score += 10
    
    # Factor 5: Nitrogen fixing bonus
    if crop_data['nitrogen_requirement'] == 'nitrogen_fixing':
        score += 10
    
    # Cap score between 10-95
    return max(10, min(95, int(score)))


def select_best_crop(crop_scores, previous_crop, used_crops, current_year, total_years, primary_goal):
    """
    Select the best crop for this year in the rotation
    """
    # Filter out recently used crops
    available_crops = {k: v for k, v in crop_scores.items()}
    
    # Ensure legume inclusion for nitrogen management
    has_legume = any(CROP_DATABASE[c]['nitrogen_requirement'] == 'nitrogen_fixing' for c in used_crops)
    
    # Force legume every 3-4 years for soil health
    if current_year % 3 == 0 or (not has_legume and current_year >= 3):
        legumes = {k: v for k, v in available_crops.items() 
                  if CROP_DATABASE[k]['nitrogen_requirement'] == 'nitrogen_fixing'}
        if legumes:
            return max(legumes, key=legumes.get)
    
    # Otherwise, select highest scoring crop
    return max(available_crops, key=available_crops.get)


def generate_crop_reasoning(crop_name, crop_data, previous_crop, year, primary_goal):
    """
    Generate human-readable reasoning for crop selection
    """
    reasons = []
    
    if crop_data['nitrogen_requirement'] == 'nitrogen_fixing':
        reasons.append(f"{crop_name} will fix nitrogen and improve soil health")
    
    if previous_crop and previous_crop in crop_data.get('good_predecessors', []):
        reasons.append(f"Excellent succession after {previous_crop}")
    
    if 'soil_health' in crop_data.get('rotation_benefits', []):
        reasons.append("Promotes long-term soil health")
    
    goal_mapping = {
        'yield_max': "High yield potential",
        'soil_health': "Soil health improvement",
        'pest_control': "Natural pest management",
        'profit_max': "Strong profit potential",
    }
    
    if primary_goal in goal_mapping:
        reasons.append(goal_mapping[primary_goal])
    
    if year == 1:
        reasons.append("Strong starter crop for rotation")
    
    return ". ".join(reasons) + "."


def calculate_rotation_benefits(rotation_sequence, primary_goal):
    """
    Calculate expected benefits from the rotation plan
    """
    benefits = []
    
    # Count nitrogen fixers
    nitrogen_fixers = sum(1 for s in rotation_sequence 
                         if s['nitrogen_requirement'] == 'nitrogen_fixing')
    
    if nitrogen_fixers >= 1:
        improvement = min(40, nitrogen_fixers * 15)
        benefits.append({
            'type': 'nitrogen_fixation',
            'improvement': improvement,
            'year': next((s['year'] for s in rotation_sequence 
                        if s['nitrogen_requirement'] == 'nitrogen_fixing'), 1),
            'description': f"Nitrogen-fixing crops will reduce fertilizer needs by approximately {improvement}%",
            'priority': 9,
        })
    
    # Crop diversity benefit
    unique_categories = len(set(CROP_DATABASE[s['crop']]['category'] for s in rotation_sequence))
    if unique_categories >= 3:
        benefits.append({
            'type': 'pest_control',
            'improvement': 25,
            'year': 2,
            'description': "Diverse crop rotation breaks pest and disease cycles",
            'priority': 8,
        })
    
    # Soil health from rotation diversity
    if len(rotation_sequence) >= 4:
        benefits.append({
            'type': 'soil_health',
            'improvement': 20,
            'year': 3,
            'description': "Multi-year rotation improves soil structure and organic matter",
            'priority': 8,
        })
    
    # Yield increase from optimized rotation
    benefits.append({
        'type': 'yield_increase',
        'improvement': 15,
        'year': 2,
        'description': "Optimized crop succession increases overall productivity",
        'priority': 7,
    })
    
    # Erosion control
    has_cover_crop = any(s['crop'] in ['Alfalfa', 'Clover'] for s in rotation_sequence)
    if has_cover_crop:
        benefits.append({
            'type': 'erosion_control',
            'improvement': 30,
            'year': 1,
            'description': "Cover crops protect soil and prevent erosion",
            'priority': 7,
        })
    
    return benefits


def generate_rotation_summary(rotation_sequence, benefits, field):
    """
    Generate a human-readable summary of the rotation plan
    """
    crops = [s['crop'] for s in rotation_sequence]
    crops_str = " → ".join(crops)
    
    total_benefit = sum(b['improvement'] for b in benefits)
    
    summary = f"This {len(rotation_sequence)}-year rotation plan for {field.name} follows the sequence: {crops_str}. "
    summary += f"Expected improvements include {len(benefits)} key benefits with an estimated {total_benefit:.0f}% cumulative improvement. "
    
    top_benefit = max(benefits, key=lambda x: x['priority'])
    summary += f"Primary benefit: {top_benefit['description']}"
    
    return summary


def create_rotation_plan_from_recommendation(field, plan_data, created_by='AI System'):
    """
    Create a RotationPlan object from recommendation data
    
    Args:
        field: Field object
        plan_data: Dictionary from generate_rotation_plan()
        created_by: User who created the plan
    
    Returns:
        Created RotationPlan object
    """
    # Create the rotation plan
    rotation_plan = RotationPlan.objects.create(
        field=field,
        name=f"AI Rotation Plan - {field.name} ({plan_data['start_year']})",
        description=plan_data['summary'],
        start_year=plan_data['start_year'],
        duration_years=plan_data['duration_years'],
        status='draft',
        primary_goal=plan_data['primary_goal'],
        ai_generated=True,
        confidence_score=plan_data['confidence_score'],
        created_by=created_by,
    )
    
    # Create sequences
    for seq_data in plan_data['sequences']:
        RotationSequence.objects.create(
            rotation_plan=rotation_plan,
            year_in_rotation=seq_data['year'],
            crop_name=seq_data['crop'],
            variety=seq_data.get('variety', ''),
            planting_season=seq_data['planting_season'],
            expected_planting_month=seq_data['planting_month'],
            expected_harvest_month=seq_data['harvest_month'],
            expected_yield_kg_per_acre=Decimal(str(sum(seq_data['expected_yield']) / 2)),
            nitrogen_requirement=seq_data['nitrogen_requirement'],
            reason_for_selection=seq_data['reasoning'],
        )
    
    # Create benefits
    for benefit_data in plan_data['benefits']:
        RotationBenefit.objects.create(
            rotation_plan=rotation_plan,
            benefit_type=benefit_data['type'],
            description=benefit_data['description'],
            expected_improvement_percent=Decimal(str(benefit_data['improvement'])),
            expected_to_manifest_year=benefit_data['year'],
            priority=benefit_data['priority'],
        )
    
    return rotation_plan


def get_active_rotation_plans(field=None):
    """
    Get all currently active rotation plans
    
    Args:
        field: Optional field to filter by
    
    Returns:
        QuerySet of active RotationPlan objects
    """
    current_year = datetime.now().year
    plans = RotationPlan.objects.filter(status='active')
    
    if field:
        plans = plans.filter(field=field)
    
    # Filter by year range
    active_plans = []
    for plan in plans:
        if plan.start_year <= current_year <= plan.get_end_year():
            active_plans.append(plan.id)
    
    return RotationPlan.objects.filter(id__in=active_plans)


def get_rotation_conflicts(field):
    """
    Check for conflicts in rotation plans for a field
    
    Returns:
        List of conflict descriptions
    """
    plans = RotationPlan.objects.filter(field=field, status__in=['active', 'draft'])
    conflicts = []
    
    if plans.count() > 1:
        # Check for overlapping year ranges
        for i, plan1 in enumerate(plans):
            for plan2 in plans[i+1:]:
                if (plan1.start_year <= plan2.get_end_year() and 
                    plan2.start_year <= plan1.get_end_year()):
                    conflicts.append(
                        f"Overlap detected: '{plan1.name}' ({plan1.start_year}-{plan1.get_end_year()}) "
                        f"conflicts with '{plan2.name}' ({plan2.start_year}-{plan2.get_end_year()})"
                    )
    
    return conflicts
