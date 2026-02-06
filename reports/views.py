"""
Reports views for PDF and CSV exports
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime

from fields.models import Field
from .pdf_utils import (
    generate_field_report_pdf,
    generate_financial_report_pdf,
    generate_all_fields_summary_pdf
)
from .csv_utils import (
    export_fields_to_csv,
    export_crop_history_to_csv,
    export_soil_analysis_to_csv,
    export_financial_records_to_csv,
    export_fields_to_excel,
    export_financial_to_excel
)


def reports_dashboard(request):
    """Main reports dashboard"""
    fields = Field.objects.all()
    
    context = {
        'fields': fields,
        'total_fields': fields.count(),
    }
    return render(request, 'reports/dashboard.html', context)


# PDF Export Views
def export_field_pdf(request, field_id):
    """Export single field report as PDF"""
    field = get_object_or_404(Field, pk=field_id)
    
    pdf = generate_field_report_pdf(field)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="field_report_{field.name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response


def export_financial_pdf(request, field_id):
    """Export financial report as PDF"""
    field = get_object_or_404(Field, pk=field_id)
    
    # Get date filters if provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
    
    pdf = generate_financial_report_pdf(field, start_date_obj, end_date_obj)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="financial_report_{field.name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response


def export_all_fields_pdf(request):
    """Export summary of all fields as PDF"""
    pdf = generate_all_fields_summary_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="farm_summary_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    return response


# CSV Export Views
def export_fields_csv(request):
    """Export all fields to CSV"""
    return export_fields_to_csv()


def export_crop_history_csv(request, field_id=None):
    """Export crop history to CSV"""
    field = get_object_or_404(Field, pk=field_id) if field_id else None
    return export_crop_history_to_csv(field)


def export_soil_csv(request, field_id=None):
    """Export soil analysis to CSV"""
    field = get_object_or_404(Field, pk=field_id) if field_id else None
    return export_soil_analysis_to_csv(field)


def export_financial_csv(request, field_id=None):
    """Export financial records to CSV"""
    field = get_object_or_404(Field, pk=field_id) if field_id else None
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
    
    return export_financial_records_to_csv(field, start_date_obj, end_date_obj)


# Excel Export Views
def export_fields_excel(request):
    """Export all fields to Excel"""
    return export_fields_to_excel()


def export_financial_excel(request, field_id=None):
    """Export financial records to Excel"""
    field = get_object_or_404(Field, pk=field_id) if field_id else None
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
    
    return export_financial_to_excel(field, start_date_obj, end_date_obj)
