from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import FinancialRecord, PerformanceMetric, YieldForecast, Report
from .forms import FinancialRecordForm, YieldForecastForm, ReportGeneratorForm, DateRangeFilterForm
from .utils import (
    calculate_financial_summary,
    calculate_yield_efficiency,
    calculate_soil_health_score,
    calculate_profitability_score,
    update_field_performance_metrics,
    get_field_comparison_data,
    generate_insights,
    generate_yield_forecast
)
from fields.models import Field, CropHistory


def analytics_dashboard(request):
    """Main analytics dashboard with comprehensive metrics"""
    
    # Get all fields
    fields = Field.objects.all()
    
    # Date range filtering
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)
    
    # Overall financial summary
    financial_summary = calculate_financial_summary(
        start_date=start_date,
        end_date=end_date
    )
    
    # Calculate totals
    total_fields = fields.count()
    total_area = sum([float(f.size_acres) for f in fields])
    
    # Recent harvests
    recent_harvests = CropHistory.objects.filter(
        harvest_date__isnull=False
    ).order_by('-harvest_date')[:10]
    
    # Get latest performance metrics
    latest_metrics = PerformanceMetric.objects.order_by('-measurement_date')[:20]
    
    # Generate insights
    insights = generate_insights()
    
    # Active forecasts
    current_year = timezone.now().year
    active_forecasts = YieldForecast.objects.filter(
        forecast_year__gte=current_year
    ).order_by('forecast_year')[:5]
    
    # Financial records by month (last 12 months)
    monthly_data = []
    for i in range(12):
        month_date = end_date - timedelta(days=30 * i)
        month_start = month_date.replace(day=1)
        
        income = FinancialRecord.objects.filter(
            transaction_type='income',
            date__year=month_start.year,
            date__month=month_start.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        expenses = FinancialRecord.objects.filter(
            transaction_type='expense',
            date__year=month_start.year,
            date__month=month_start.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        monthly_data.insert(0, {
            'month': month_start.strftime('%b %Y'),
            'income': float(income),
            'expenses': float(expenses),
            'profit': float(income - expenses)
        })
    
    context = {
        'total_fields': total_fields,
        'total_area': total_area,
        'financial_summary': financial_summary,
        'recent_harvests': recent_harvests,
        'latest_metrics': latest_metrics,
        'insights': insights[:10],  # Top 10 insights
        'active_forecasts': active_forecasts,
        'monthly_data': monthly_data,
    }
    
    return render(request, 'analytics/analytics_dashboard.html', context)


def financial_overview(request):
    """Detailed financial analytics view"""
    
    # Handle filtering
    filter_form = DateRangeFilterForm(request.GET or None)
    
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=365)
    selected_field = None
    
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('start_date'):
            start_date = filter_form.cleaned_data['start_date']
        if filter_form.cleaned_data.get('end_date'):
            end_date = filter_form.cleaned_data['end_date']
        if filter_form.cleaned_data.get('field'):
            selected_field = filter_form.cleaned_data['field']
    
    # Get financial summary
    financial_summary = calculate_financial_summary(
        field=selected_field,
        start_date=start_date,
        end_date=end_date
    )
    
    # Get all records
    records = FinancialRecord.objects.all()
    
    if selected_field:
        records = records.filter(Q(field=selected_field) | Q(field__isnull=True))
    
    records = records.filter(date__gte=start_date, date__lte=end_date).order_by('-date')
    
    # Category breakdown for charts
    expense_categories = list(financial_summary['expense_by_category'])
    income_categories = list(financial_summary['income_by_category'])
    
    context = {
        'filter_form': filter_form,
        'financial_summary': financial_summary,
        'records': records[:50],  # Latest 50 records
        'expense_categories': expense_categories,
        'income_categories': income_categories,
        'start_date': start_date,
        'end_date': end_date,
        'selected_field': selected_field,
    }
    
    return render(request, 'analytics/financial_overview.html', context)


def financial_record_create(request):
    """Create new financial record"""
    
    if request.method == 'POST':
        form = FinancialRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, f'Financial record created successfully!')
            return redirect('analytics:financial_overview')
    else:
        form = FinancialRecordForm()
    
    context = {
        'form': form,
        'title': 'Add Financial Record'
    }
    
    return render(request, 'analytics/financial_record_form.html', context)


def financial_record_update(request, pk):
    """Update existing financial record"""
    
    record = get_object_or_404(FinancialRecord, pk=pk)
    
    if request.method == 'POST':
        form = FinancialRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Financial record updated successfully!')
            return redirect('analytics:financial_overview')
    else:
        form = FinancialRecordForm(instance=record)
    
    context = {
        'form': form,
        'record': record,
        'title': 'Edit Financial Record'
    }
    
    return render(request, 'analytics/financial_record_form.html', context)


def financial_record_delete(request, pk):
    """Delete financial record"""
    
    record = get_object_or_404(FinancialRecord, pk=pk)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Financial record deleted successfully!')
        return redirect('analytics:financial_overview')
    
    context = {
        'record': record
    }
    
    return render(request, 'analytics/financial_record_confirm_delete.html', context)


def yield_analysis(request):
    """Yield analysis and forecasting view"""
    
    # Get all fields
    fields = Field.objects.all()
    
    # Historical yield data by field
    field_yield_data = []
    
    for field in fields:
        harvests = CropHistory.objects.filter(
            field=field,
            yield_amount__gt=0
        ).order_by('-harvest_date')[:10]
        
        if harvests:
            avg_yield = sum([float(h.yield_amount) for h in harvests]) / len(harvests)
            latest_yield = float(harvests[0].yield_amount) if harvests else 0
            
            field_yield_data.append({
                'field': field,
                'avg_yield': round(avg_yield, 2),
                'latest_yield': round(latest_yield, 2),
                'harvest_count': len(harvests),
                'trend': 'up' if latest_yield > avg_yield else 'down'
            })
    
    # Active forecasts
    forecasts = YieldForecast.objects.filter(
        forecast_year__gte=timezone.now().year
    ).select_related('field').order_by('forecast_year', 'field')
    
    # Forecast accuracy (completed forecasts)
    completed_forecasts = YieldForecast.objects.filter(
        actual_yield_kg__isnull=False
    ).order_by('-forecast_year')[:10]
    
    context = {
        'field_yield_data': field_yield_data,
        'forecasts': forecasts,
        'completed_forecasts': completed_forecasts,
    }
    
    return render(request, 'analytics/yield_analysis.html', context)


def yield_forecast_create(request):
    """Create new yield forecast"""
    
    if request.method == 'POST':
        form = YieldForecastForm(request.POST)
        if form.is_valid():
            forecast = form.save()
            messages.success(request, 'Yield forecast created successfully!')
            return redirect('analytics:yield_analysis')
    else:
        form = YieldForecastForm()
    
    context = {
        'form': form,
        'title': 'Create Yield Forecast'
    }
    
    return render(request, 'analytics/yield_forecast_form.html', context)


def yield_forecast_update(request, pk):
    """Update yield forecast"""
    
    forecast = get_object_or_404(YieldForecast, pk=pk)
    
    if request.method == 'POST':
        form = YieldForecastForm(request.POST, instance=forecast)
        if form.is_valid():
            forecast = form.save()
            # Calculate variance if actual yield is provided
            if forecast.actual_yield_kg:
                forecast.calculate_variance()
                forecast.save()
            messages.success(request, 'Yield forecast updated successfully!')
            return redirect('analytics:yield_analysis')
    else:
        form = YieldForecastForm(instance=forecast)
    
    context = {
        'form': form,
        'forecast': forecast,
        'title': 'Update Yield Forecast'
    }
    
    return render(request, 'analytics/yield_forecast_form.html', context)


def performance_metrics_view(request):
    """View and compare performance metrics across fields"""
    
    fields = Field.objects.all()
    
    # Get latest metrics for each field
    field_performance = []
    
    for field in fields:
        # Update metrics
        update_field_performance_metrics(field)
        
        # Get latest metrics
        latest_metrics = PerformanceMetric.objects.filter(
            field=field
        ).order_by('-measurement_date')[:10]
        
        metrics_by_type = {}
        for metric in latest_metrics:
            if metric.metric_type not in metrics_by_type:
                metrics_by_type[metric.metric_type] = metric
        
        field_performance.append({
            'field': field,
            'metrics': metrics_by_type
        })
    
    # Get field comparison data
    comparison_data = get_field_comparison_data(fields)
    
    context = {
        'field_performance': field_performance,
        'comparison_data': comparison_data,
    }
    
    return render(request, 'analytics/performance_metrics.html', context)


def insights_view(request):
    """View AI-generated insights and recommendations"""
    
    # Generate all insights
    all_insights = generate_insights()
    
    # Categorize insights
    insights_by_category = {
        'soil_health': [],
        'yield': [],
        'rotation': [],
        'financial': [],
        'other': []
    }
    
    for insight in all_insights:
        category = insight.get('category', 'other')
        if category in insights_by_category:
            insights_by_category[category].append(insight)
        else:
            insights_by_category['other'].append(insight)
    
    # Count by priority
    high_priority = len([i for i in all_insights if i.get('priority') == 'high'])
    medium_priority = len([i for i in all_insights if i.get('priority') == 'medium'])
    low_priority = len([i for i in all_insights if i.get('priority') == 'low'])
    
    context = {
        'insights_by_category': insights_by_category,
        'total_insights': len(all_insights),
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
    }
    
    return render(request, 'analytics/insights.html', context)
