from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime

from .models import RotationPlan, RotationSequence, RotationBenefit
from .forms import RotationPlanForm, RotationSequenceForm, RotationBenefitForm, GenerateRotationForm
from .utils import (
    generate_rotation_plan,
    create_rotation_plan_from_recommendation,
    get_active_rotation_plans,
    get_rotation_conflicts,
)
from fields.models import Field


# ==================== ROTATION PLAN VIEWS ====================

def rotation_plan_list(request):
    """List all rotation plans with filtering and statistics"""
    plans = RotationPlan.objects.all().select_related('field')
    
    # Filtering
    field_id = request.GET.get('field')
    status = request.GET.get('status')
    primary_goal = request.GET.get('primary_goal')
    
    if field_id:
        plans = plans.filter(field_id=field_id)
    if status:
        plans = plans.filter(status=status)
    if primary_goal:
        plans = plans.filter(primary_goal=primary_goal)
    
    # Statistics
    stats = {
        'total_plans': RotationPlan.objects.count(),
        'active_plans': RotationPlan.objects.filter(status='active').count(),
        'ai_generated': RotationPlan.objects.filter(ai_generated=True).count(),
        'avg_confidence': RotationPlan.objects.filter(ai_generated=True).aggregate(
            Avg('confidence_score')
        )['confidence_score__avg'] or 0,
    }
    
    # Get all fields for filter dropdown
    fields = Field.objects.all().order_by('name')
    
    context = {
        'plans': plans,
        'stats': stats,
        'fields': fields,
        'selected_field': field_id,
        'selected_status': status,
        'selected_goal': primary_goal,
        'status_choices': RotationPlan._meta.get_field('status').choices,
        'goal_choices': RotationPlan._meta.get_field('primary_goal').choices,
    }
    
    return render(request, 'rotation/rotation_plan_list.html', context)


def rotation_plan_detail(request, pk):
    """Detailed view of a rotation plan"""
    plan = get_object_or_404(RotationPlan.objects.select_related('field'), pk=pk)
    sequences = plan.sequences.all().order_by('year_in_rotation')
    benefits = plan.benefits.all().order_by('-priority', 'expected_to_manifest_year')
    
    # Check for conflicts
    conflicts = get_rotation_conflicts(plan.field)
    
    # Get field's soil and weather data for context
    latest_soil = plan.field.soil_analyses.order_by('-analysis_date').first()
    latest_weather = plan.field.weather_data.order_by('-date').first() if hasattr(plan.field, 'weather_data') else None
    
    # Calculate progress
    current_year = datetime.now().year
    if plan.start_year <= current_year <= plan.get_end_year():
        progress_years = current_year - plan.start_year + 1
        progress_percent = (progress_years / plan.duration_years) * 100
    else:
        progress_percent = 0
    
    context = {
        'plan': plan,
        'sequences': sequences,
        'benefits': benefits,
        'conflicts': conflicts,
        'latest_soil': latest_soil,
        'latest_weather': latest_weather,
        'progress_percent': progress_percent,
        'is_active': plan.is_active(),
        'current_sequence': plan.get_current_year_sequence(),
    }
    
    return render(request, 'rotation/rotation_plan_detail.html', context)


def rotation_plan_create(request):
    """Create a new rotation plan manually"""
    if request.method == 'POST':
        form = RotationPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.ai_generated = False
            plan.save()
            messages.success(request, f'Rotation plan "{plan.name}" created successfully!')
            return redirect('rotation:plan_detail', pk=plan.pk)
    else:
        form = RotationPlanForm()
    
    context = {
        'form': form,
        'title': 'Create Rotation Plan',
    }
    
    return render(request, 'rotation/rotation_plan_form.html', context)


def rotation_plan_update(request, pk):
    """Update an existing rotation plan"""
    plan = get_object_or_404(RotationPlan, pk=pk)
    
    if request.method == 'POST':
        form = RotationPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, f'Rotation plan "{plan.name}" updated successfully!')
            return redirect('rotation:plan_detail', pk=plan.pk)
    else:
        form = RotationPlanForm(instance=plan)
    
    context = {
        'form': form,
        'plan': plan,
        'title': 'Edit Rotation Plan',
    }
    
    return render(request, 'rotation/rotation_plan_form.html', context)


def rotation_plan_delete(request, pk):
    """Delete a rotation plan"""
    plan = get_object_or_404(RotationPlan, pk=pk)
    
    if request.method == 'POST':
        plan_name = plan.name
        plan.delete()
        messages.success(request, f'Rotation plan "{plan_name}" deleted successfully!')
        return redirect('rotation:plan_list')
    
    context = {
        'plan': plan,
        'sequences_count': plan.sequences.count(),
        'benefits_count': plan.benefits.count(),
    }
    
    return render(request, 'rotation/rotation_plan_confirm_delete.html', context)


# ==================== SEQUENCE VIEWS ====================

def sequence_create(request, plan_id):
    """Add a crop sequence to a rotation plan"""
    plan = get_object_or_404(RotationPlan, pk=plan_id)
    
    if request.method == 'POST':
        form = RotationSequenceForm(request.POST)
        if form.is_valid():
            sequence = form.save()
            messages.success(request, f'Added {sequence.crop_name} to year {sequence.year_in_rotation}')
            return redirect('rotation:plan_detail', pk=plan.pk)
    else:
        # Pre-fill rotation_plan and suggest next year
        next_year = plan.sequences.count() + 1
        form = RotationSequenceForm(initial={
            'rotation_plan': plan,
            'year_in_rotation': next_year,
        })
    
    context = {
        'form': form,
        'plan': plan,
        'title': f'Add Crop to {plan.name}',
    }
    
    return render(request, 'rotation/rotation_sequence_form.html', context)


def sequence_update(request, pk):
    """Edit a rotation sequence"""
    sequence = get_object_or_404(RotationSequence, pk=pk)
    
    if request.method == 'POST':
        form = RotationSequenceForm(request.POST, instance=sequence)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated {sequence.crop_name} in year {sequence.year_in_rotation}')
            return redirect('rotation:plan_detail', pk=sequence.rotation_plan.pk)
    else:
        form = RotationSequenceForm(instance=sequence)
    
    context = {
        'form': form,
        'sequence': sequence,
        'title': f'Edit Year {sequence.year_in_rotation} - {sequence.crop_name}',
    }
    
    return render(request, 'rotation/rotation_sequence_form.html', context)


def sequence_delete(request, pk):
    """Delete a rotation sequence"""
    sequence = get_object_or_404(RotationSequence, pk=pk)
    plan_pk = sequence.rotation_plan.pk
    
    if request.method == 'POST':
        crop_name = sequence.crop_name
        year = sequence.year_in_rotation
        sequence.delete()
        messages.success(request, f'Removed {crop_name} from year {year}')
        return redirect('rotation:plan_detail', pk=plan_pk)
    
    context = {
        'sequence': sequence,
    }
    
    return render(request, 'rotation/rotation_sequence_confirm_delete.html', context)


def sequence_mark_complete(request, pk):
    """Mark a sequence as completed"""
    sequence = get_object_or_404(RotationSequence, pk=pk)
    sequence.is_completed = True
    sequence.save()
    messages.success(request, f'{sequence.crop_name} marked as completed!')
    return redirect('rotation:plan_detail', pk=sequence.rotation_plan.pk)


# ==================== BENEFIT VIEWS ====================

def benefit_create(request, plan_id):
    """Add a expected benefit to a rotation plan"""
    plan = get_object_or_404(RotationPlan, pk=plan_id)
    
    if request.method == 'POST':
        form = RotationBenefitForm(request.POST)
        if form.is_valid():
            benefit = form.save()
            messages.success(request, f'Added benefit: {benefit.get_benefit_type_display()}')
            return redirect('rotation:plan_detail', pk=plan.pk)
    else:
        form = RotationBenefitForm(initial={'rotation_plan': plan})
    
    context = {
        'form': form,
        'plan': plan,
        'title': f'Add Benefit to {plan.name}',
    }
    
    return render(request, 'rotation/rotation_benefit_form.html', context)


def benefit_update(request, pk):
    """Update a rotation benefit (e.g., add verification data)"""
    benefit = get_object_or_404(RotationBenefit, pk=pk)
    
    if request.method == 'POST':
        form = RotationBenefitForm(request.POST, instance=benefit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Benefit updated successfully!')
            return redirect('rotation:plan_detail', pk=benefit.rotation_plan.pk)
    else:
        form = RotationBenefitForm(instance=benefit)
    
    context = {
        'form': form,
        'benefit': benefit,
        'title': f'Update {benefit.get_benefit_type_display()}',
    }
    
    return render(request, 'rotation/rotation_benefit_form.html', context)


def benefit_list(request):
    """View all rotation benefits across all plans"""
    benefits = RotationBenefit.objects.all().select_related('rotation_plan', 'rotation_plan__field')
    
    # Filtering
    benefit_type = request.GET.get('benefit_type')
    is_verified = request.GET.get('is_verified')
    
    if benefit_type:
        benefits = benefits.filter(benefit_type=benefit_type)
    if is_verified == 'true':
        benefits = benefits.filter(is_verified=True)
    elif is_verified == 'false':
        benefits = benefits.filter(is_verified=False)
    
    # Statistics
    stats = {
        'total_benefits': RotationBenefit.objects.count(),
        'verified_benefits': RotationBenefit.objects.filter(is_verified=True).count(),
        'avg_expected_improvement': RotationBenefit.objects.aggregate(
            Avg('expected_improvement_percent')
        )['expected_improvement_percent__avg'] or 0,
        'avg_actual_improvement': RotationBenefit.objects.filter(
            is_verified=True
        ).aggregate(
            Avg('actual_improvement_percent')
        )['actual_improvement_percent__avg'] or 0,
    }
    
    context = {
        'benefits': benefits,
        'stats': stats,
        'benefit_type_choices': RotationBenefit._meta.get_field('benefit_type').choices,
        'selected_type': benefit_type,
        'selected_verified': is_verified,
    }
    
    return render(request, 'rotation/rotation_benefit_list.html', context)


# ==================== AI GENERATION VIEWS ====================

def generate_rotation_view(request):
    """Generate AI-powered rotation recommendation"""
    if request.method == 'POST':
        form = GenerateRotationForm(request.POST)
        if form.is_valid():
            field = form.cleaned_data['field']
            duration_years = form.cleaned_data['duration_years']
            start_year = form.cleaned_data['start_year']
            primary_goal = form.cleaned_data['primary_goal']
            
            # Generate the recommendation
            try:
                plan_data = generate_rotation_plan(
                    field=field,
                    duration_years=duration_years,
                    primary_goal=primary_goal,
                    start_year=start_year
                )
                
                # Create the rotation plan
                rotation_plan = create_rotation_plan_from_recommendation(
                    field=field,
                    plan_data=plan_data,
                    created_by=request.user.username if request.user.is_authenticated else 'AI System'
                )
                
                messages.success(
                    request,
                    f'AI rotation plan generated with {plan_data["confidence_score"]}% confidence!'
                )
                return redirect('rotation:plan_detail', pk=rotation_plan.pk)
            
            except Exception as e:
                messages.error(request, f'Error generating rotation plan: {str(e)}')
    else:
        form = GenerateRotationForm()
    
    context = {
        'form': form,
        'title': 'Generate AI Rotation Plan',
    }
    
    return render(request, 'rotation/generate_rotation.html', context)


def rotation_dashboard(request):
    """Main rotation dashboard with overview"""
    current_year = datetime.now().year
    
    # Active plans
    active_plans = get_active_rotation_plans()
    
    # Upcoming activities (from active plans)
    upcoming_sequences = RotationSequence.objects.filter(
        rotation_plan__status='active',
        is_completed=False,
    ).select_related('rotation_plan', 'rotation_plan__field')
    
    # Filter by current year context
    current_sequences = [
        seq for seq in upcoming_sequences 
        if seq.get_actual_year() == current_year
    ]
    
    # Benefits summary
    total_benefits = RotationBenefit.objects.count()
    verified_benefits = RotationBenefit.objects.filter(is_verified=True).count()
    
    # Recent plans
    recent_plans = RotationPlan.objects.all().order_by('-created_at')[:5]
    
    # Fields without rotation plans
    fields_without_rotation = Field.objects.filter(
        Q(rotation_plans__isnull=True) | 
        ~Q(rotation_plans__status__in=['active', 'draft'])
    ).distinct()
    
    context = {
        'active_plans_count': active_plans.count(),
        'active_plans': active_plans[:5],
        'current_sequences': current_sequences[:10],
        'total_benefits': total_benefits,
        'verified_benefits': verified_benefits,
        'recent_plans': recent_plans,
        'fields_without_rotation': fields_without_rotation[:5],
        'total_plans': RotationPlan.objects.count(),
    }
    
    return render(request, 'rotation/rotation_dashboard.html', context)


# ==================== API VIEWS ====================

def rotation_timeline_data(request, pk):
    """Get JSON data for rotation timeline visualization"""
    plan = get_object_or_404(RotationPlan, pk=pk)
    sequences = plan.sequences.all().order_by('year_in_rotation')
    
    timeline_data = []
    for seq in sequences:
        timeline_data.append({
            'year': seq.get_actual_year(),
            'year_in_rotation': seq.year_in_rotation,
            'crop': seq.crop_name,
            'variety': seq.variety or '',
            'planting_month': seq.expected_planting_month,
            'harvest_month': seq.expected_harvest_month,
            'expected_yield': float(seq.expected_yield_kg_per_acre or 0),
            'nitrogen_requirement': seq.nitrogen_requirement,
            'is_completed': seq.is_completed,
        })
    
    return JsonResponse({
        'plan_name': plan.name,
        'start_year': plan.start_year,
        'end_year': plan.get_end_year(),
        'timeline': timeline_data,
    })
