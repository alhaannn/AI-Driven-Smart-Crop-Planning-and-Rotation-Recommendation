"""
Analytics utility functions for calculating metrics, generating insights, and creating forecasts
"""
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum, Avg, Count, Q, Max, Min
from django.utils import timezone
from fields.models import Field, CropHistory
from soil.models import SoilAnalysis
from rotation.models import RotationPlan, RotationSequence
from analytics.models import FinancialRecord, PerformanceMetric, YieldForecast
import statistics


def calculate_financial_summary(field=None, start_date=None, end_date=None):
    """
    Calculate comprehensive financial summary
    """
    queryset = FinancialRecord.objects.all()
    
    if field:
        queryset = queryset.filter(Q(field=field) | Q(field__isnull=True))
    
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    
    if end_date:
        queryset = queryset.filter(date__lte=end_date)
    
    total_income = queryset.filter(transaction_type='income').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    
    total_expenses = queryset.filter(transaction_type='expense').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    
    total_investments = queryset.filter(transaction_type='investment').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    
    net_profit = total_income - total_expenses
    roi = ((net_profit / total_investments) * 100) if total_investments > 0 else Decimal('0.00')
    
    # Category breakdown
    expense_by_category = queryset.filter(transaction_type='expense').values(
        'category').annotate(total=Sum('amount')).order_by('-total')
    
    income_by_category = queryset.filter(transaction_type='income').values(
        'category').annotate(total=Sum('amount')).order_by('-total')
    
    return {
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'total_investments': float(total_investments),
        'net_profit': float(net_profit),
        'roi_percent': float(roi),
        'expense_by_category': list(expense_by_category),
        'income_by_category': list(income_by_category),
        'profit_margin': float((net_profit / total_income * 100) if total_income > 0 else 0),
    }


def calculate_yield_efficiency(field):
    """
    Calculate yield efficiency score for a field based on historical data
    """
    recent_harvests = CropHistory.objects.filter(
        field=field,
        harvest_date__isnull=False,
        yield_amount__gt=0
    ).order_by('-harvest_date')[:10]
    
    if not recent_harvests:
        return {
            'score': 0,
            'trend': 'no_data',
            'average_yield': 0,
            'details': 'No harvest data available'
        }
    
    yields = [float(h.yield_amount) for h in recent_harvests]
    avg_yield = statistics.mean(yields)
    
    # Calculate trend (comparing recent vs older harvests)
    if len(yields) >= 4:
        recent_avg = statistics.mean(yields[:len(yields)//2])
        older_avg = statistics.mean(yields[len(yields)//2:])
        trend = 'improving' if recent_avg > older_avg else 'declining'
    else:
        trend = 'stable'
    
    # Calculate score based on consistency and average
    if len(yields) > 1:
        std_dev = statistics.stdev(yields)
        consistency_score = max(0, 100 - (std_dev / avg_yield * 100))
    else:
        consistency_score = 50
    
    # Combine factors for final score
    score = min(100, consistency_score * 0.6 + (avg_yield / 5000 * 100) * 0.4)
    
    return {
        'score': round(score, 2),
        'trend': trend,
        'average_yield': round(avg_yield, 2),
        'consistency': round(consistency_score, 2),
        'details': f'Based on {len(yields)} recent harvests'
    }


def calculate_soil_health_score(field):
    """
    Calculate soil health score based on recent soil analyses
    """
    latest_analysis = SoilAnalysis.objects.filter(field=field).order_by('-analysis_date').first()
    
    if not latest_analysis:
        return {
            'score': 0,
            'details': 'No soil analysis data available'
        }
    
    score = 0
    factors = []
    
    # pH level (ideal: 6.0-7.0)
    ph = float(latest_analysis.ph_level)
    if 6.0 <= ph <= 7.0:
        ph_score = 100
    elif 5.5 <= ph < 6.0 or 7.0 < ph <= 7.5:
        ph_score = 80
    elif 5.0 <= ph < 5.5 or 7.5 < ph <= 8.0:
        ph_score = 60
    else:
        ph_score = 40
    
    factors.append({'name': 'pH Level', 'score': ph_score, 'value': ph})
    score += ph_score * 0.25
    
    # Nitrogen (good: >40 ppm)
    n = float(latest_analysis.nitrogen_ppm)
    n_score = min(100, (n / 60) * 100) if n > 0 else 0
    factors.append({'name': 'Nitrogen', 'score': n_score, 'value': n})
    score += n_score * 0.25
    
    # Phosphorus (good: >30 ppm)
    p = float(latest_analysis.phosphorus_ppm)
    p_score = min(100, (p / 50) * 100) if p > 0 else 0
    factors.append({'name': 'Phosphorus', 'score': p_score, 'value': p})
    score += p_score * 0.25
    
    # Potassium (good: >200 ppm)
    k = float(latest_analysis.potassium_ppm)
    k_score = min(100, (k / 300) * 100) if k > 0 else 0
    factors.append({'name': 'Potassium', 'score': k_score, 'value': k})
    score += k_score * 0.25
    
    return {
        'score': round(score, 2),
        'factors': factors,
        'analysis_date': latest_analysis.analysis_date,
        'details': 'Based on latest soil analysis'
    }


def calculate_profitability_score(field, year=None):
    """
    Calculate profitability score for a field
    """
    if year is None:
        year = timezone.now().year
    
    # Get financial data for the year
    records = FinancialRecord.objects.filter(field=field, date__year=year)
    
    income = records.filter(transaction_type='income').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    
    expenses = records.filter(transaction_type='expense').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    
    if expenses == 0:
        return {
            'score': 0,
            'details': 'No financial data available'
        }
    
    profit = income - expenses
    profit_margin = (profit / income * 100) if income > 0 else Decimal('-100')
    
    # Score based on profit margin
    if profit_margin >= 40:
        score = 100
    elif profit_margin >= 25:
        score = 80
    elif profit_margin >= 10:
        score = 60
    elif profit_margin >= 0:
        score = 40
    else:
        score = 20
    
    return {
        'score': score,
        'profit': float(profit),
        'profit_margin': float(profit_margin),
        'income': float(income),
        'expenses': float(expenses),
        'details': f'Based on {year} financial data'
    }


def calculate_rotation_adherence(field):
    """
    Calculate how well the field adheres to rotation plans
    """
    active_plan = RotationPlan.objects.filter(field=field, status='active').first()
    
    if not active_plan:
        return {
            'score': 0,
            'details': 'No active rotation plan'
        }
    
    sequences = RotationSequence.objects.filter(rotation_plan=active_plan)
    total = sequences.count()
    
    if total == 0:
        return {
            'score': 0,
            'details': 'No rotation sequences defined'
        }
    
    completed = sequences.filter(is_completed=True).count()
    adherence_rate = (completed / total) * 100
    
    # Check for delays
    current_year = timezone.now().year
    overdue = sequences.filter(
        is_completed=False,
        year_in_rotation__lt=(current_year - active_plan.start_year + 1)
    ).count()
    
    # Penalize for overdue sequences
    score = adherence_rate - (overdue * 10)
    score = max(0, min(100, score))
    
    return {
        'score': round(score, 2),
        'completed': completed,
        'total': total,
        'overdue': overdue,
        'adherence_rate': round(adherence_rate, 2),
        'details': f'{completed}/{total} sequences completed'
    }


def generate_yield_forecast(field, crop_name, forecast_year, planting_season):
    """
    Generate yield forecast based on historical data
    """
    # Get historical yields for the same crop on this field
    historical = CropHistory.objects.filter(
        field=field,
        crop_name=crop_name,
        yield_amount__gt=0
    ).order_by('-harvest_date')[:5]
    
    if not historical:
        # Use default estimate
        predicted_yield = Decimal('3000.00')  # 3000 kg default
        confidence = 40
        method = 'expert_estimate'
    elif len(historical) == 1:
        predicted_yield = historical[0].yield_amount
        confidence = 60
        method = 'historical_average'
    else:
        # Calculate trend-based forecast
        yields = [float(h.yield_amount) for h in historical]
        avg_yield = statistics.mean(yields)
        
        # Check for trend
        if len(yields) >= 3:
            recent_avg = statistics.mean(yields[:2])
            older_avg = statistics.mean(yields[-2:])
            
            if recent_avg > older_avg:
                # Improving trend - increase prediction
                predicted_yield = Decimal(str(avg_yield * 1.05))
            else:
                # Declining trend - decrease prediction
                predicted_yield = Decimal(str(avg_yield * 0.95))
            
            confidence = 75
            method = 'trend_analysis'
        else:
            predicted_yield = Decimal(str(avg_yield))
            confidence = 70
            method = 'historical_average'
    
    # Consider soil health
    soil_score = calculate_soil_health_score(field)
    if soil_score['score'] > 0:
        soil_factor = soil_score['score'] / 100
        predicted_yield = predicted_yield * Decimal(str(soil_factor))
        confidence = min(95, confidence + 10)
    
    total_predicted = predicted_yield * Decimal(str(field.size_acres))
    
    factors = {
        'historical_harvests': len(historical),
        'soil_health_score': soil_score['score'],
        'field_size_acres': float(field.size_acres),
        'prediction_basis': method
    }
    
    # Create or update forecast
    forecast, created = YieldForecast.objects.update_or_create(
        field=field,
        crop_name=crop_name,
        forecast_year=forecast_year,
        planting_season=planting_season,
        defaults={
            'predicted_yield_kg': total_predicted,
            'confidence_level': confidence,
            'prediction_method': method,
            'factors_considered': factors
        }
    )
    
    return forecast


def update_field_performance_metrics(field):
    """
    Calculate and update all performance metrics for a field
    """
    current_date = timezone.now().date()
    current_year = current_date.year
    
    metrics_data = {
        'yield_efficiency': calculate_yield_efficiency(field),
        'soil_health_score': calculate_soil_health_score(field),
        'profitability': calculate_profitability_score(field, current_year),
        'rotation_adherence': calculate_rotation_adherence(field),
    }
    
    created_metrics = []
    
    for metric_type, data in metrics_data.items():
        if data['score'] > 0:
            metric, created = PerformanceMetric.objects.update_or_create(
                field=field,
                metric_type=metric_type,
                measurement_date=current_date,
                defaults={
                    'score': Decimal(str(data['score'])),
                    'year': current_year,
                    'month': current_date.month,
                    'calculation_details': data,
                    'notes': data.get('details', '')
                }
            )
            created_metrics.append(metric)
    
    return created_metrics


def get_field_comparison_data(fields):
    """
    Compare performance across multiple fields
    """
    comparison = []
    
    for field in fields:
        latest_metrics = PerformanceMetric.objects.filter(field=field).order_by('-measurement_date')[:10]
        
        metrics_by_type = {}
        for metric in latest_metrics:
            if metric.metric_type not in metrics_by_type:
                metrics_by_type[metric.metric_type] = metric
        
        # Get financial summary
        financial = calculate_financial_summary(field=field, start_date=timezone.now().date() - timedelta(days=365))
        
        # Get latest yield
        latest_harvest = CropHistory.objects.filter(field=field).order_by('-harvest_date').first()
        
        comparison.append({
            'field': field,
            'metrics': metrics_by_type,
            'financial': financial,
            'latest_yield': latest_harvest.yield_amount if latest_harvest else 0,
            'total_area': field.size_acres
        })
    
    return comparison


def generate_insights(field=None):
    """
    Generate AI-like insights and recommendations
    """
    insights = []
    
    if field:
        fields = [field]
    else:
        fields = Field.objects.all()
    
    for f in fields:
        # Soil health insights
        soil_score = calculate_soil_health_score(f)
        if soil_score['score'] < 60:
            insights.append({
                'type': 'warning',
                'category': 'soil_health',
                'field': f,
                'message': f"Soil health score is low ({soil_score['score']}%). Consider soil amendments.",
                'priority': 'high'
            })
        
        # Yield efficiency insights
        yield_eff = calculate_yield_efficiency(f)
        if yield_eff['trend'] == 'declining':
            insights.append({
                'type': 'alert',
                'category': 'yield',
                'field': f,
                'message': f"Yield efficiency is declining. Review crop rotation and fertilization strategies.",
                'priority': 'medium'
            })
        
        # Rotation adherence insights
        rotation = calculate_rotation_adherence(f)
        if rotation['score'] < 70 and rotation['score'] > 0:
            insights.append({
                'type': 'info',
                'category': 'rotation',
                'field': f,
                'message': f"Rotation plan adherence is {rotation['score']}%. {rotation['overdue']} sequences overdue.",
                'priority': 'medium'
            })
    
    return insights
