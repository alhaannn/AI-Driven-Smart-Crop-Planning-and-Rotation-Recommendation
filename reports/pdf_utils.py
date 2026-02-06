"""
PDF Report Generation utilities using ReportLab
"""
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from decimal import Decimal


def generate_field_report_pdf(field):
    """Generate comprehensive PDF report for a field"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph(f"Field Report: {field.name}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Field Information Table
    field_data = [
        ['Field Information', ''],
        ['Location', field.location],
        ['Size', f'{field.size_acres} acres'],
        ['Soil Type', field.soil_type],
        ['Irrigation', field.irrigation_type],
        ['Created', field.created_at.strftime('%B %d, %Y')],
    ]
    
    field_table = Table(field_data, colWidths=[2*inch, 4*inch])
    field_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ]))
    elements.append(field_table)
    elements.append(Spacer(1, 20))
    
    # Crop History
    crop_histories = field.crop_histories.all()[:10]
    if crop_histories:
        elements.append(Paragraph("Crop History", heading_style))
        
        crop_data = [['Crop', 'Variety', 'Planting Date', 'Harvest Date', 'Yield (kg/acre)']]
        for crop in crop_histories:
            crop_data.append([
                crop.crop_name,
                crop.variety or 'N/A',
                crop.planting_date.strftime('%d-%b-%Y'),
                crop.harvest_date.strftime('%d-%b-%Y'),
                f'{crop.yield_amount}'
            ])
        
        crop_table = Table(crop_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.1*inch])
        crop_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(crop_table)
        elements.append(Spacer(1, 20))
    
    # Soil Analysis
    soil_analyses = field.soil_analyses.all()[:5]
    if soil_analyses:
        elements.append(Paragraph("Recent Soil Analysis", heading_style))
        
        soil_data = [['Date', 'pH', 'N (ppm)', 'P (ppm)', 'K (ppm)', 'Organic Matter %']]
        for soil in soil_analyses:
            soil_data.append([
                soil.analysis_date.strftime('%d-%b-%Y'),
                f'{soil.ph_level}',
                f'{soil.nitrogen_ppm}',
                f'{soil.phosphorus_ppm}',
                f'{soil.potassium_ppm}',
                f'{soil.organic_matter}'
            ])
        
        soil_table = Table(soil_data, colWidths=[1.2*inch, 0.8*inch, 0.9*inch, 0.9*inch, 0.9*inch, 1.1*inch])
        soil_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgoldenrodyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(soil_table)
        elements.append(Spacer(1, 20))
    
    # Footer
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(Spacer(1, 30))
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and return it
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_financial_report_pdf(field, start_date=None, end_date=None):
    """Generate financial report PDF for a field"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    title = Paragraph(f"Financial Report: {field.name}", title_style)
    elements.append(title)
    
    # Date range if provided
    if start_date and end_date:
        date_range = Paragraph(
            f"Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}",
            styles['Normal']
        )
        elements.append(date_range)
    
    elements.append(Spacer(1, 20))
    
    # Get financial records
    from analytics.models import FinancialRecord
    records = FinancialRecord.objects.filter(field=field)
    
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)
    
    # Calculate summary
    income_records = records.filter(transaction_type='income')
    expense_records = records.filter(transaction_type='expense')
    
    total_income = sum(r.amount for r in income_records)
    total_expenses = sum(r.amount for r in expense_records)
    net_profit = total_income - total_expenses
    
    # Summary Table
    summary_data = [
        ['Financial Summary', ''],
        ['Total Income', f'₹ {total_income:,.2f}'],
        ['Total Expenses', f'₹ {total_expenses:,.2f}'],
        ['Net Profit/Loss', f'₹ {net_profit:,.2f}'],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Income Details
    if income_records:
        elements.append(Paragraph("Income Transactions", heading_style))
        income_data = [['Date', 'Category', 'Description', 'Amount (₹)']]
        for record in income_records:
            income_data.append([
                record.date.strftime('%d-%b-%Y'),
                record.get_category_display(),
                record.description[:30] if record.description else 'N/A',
                f'{record.amount:,.2f}'
            ])
        
        income_table = Table(income_data, colWidths=[1.2*inch, 1.5*inch, 2.3*inch, 1.2*inch])
        income_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(income_table)
        elements.append(Spacer(1, 20))
    
    # Expense Details
    if expense_records:
        elements.append(Paragraph("Expense Transactions", heading_style))
        expense_data = [['Date', 'Category', 'Description', 'Amount (₹)']]
        for record in expense_records:
            expense_data.append([
                record.date.strftime('%d-%b-%Y'),
                record.get_category_display(),
                record.description[:30] if record.description else 'N/A',
                f'{record.amount:,.2f}'
            ])
        
        expense_table = Table(expense_data, colWidths=[1.2*inch, 1.5*inch, 2.3*inch, 1.2*inch])
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(expense_table)
    
    # Footer
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(Spacer(1, 30))
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_all_fields_summary_pdf():
    """Generate summary PDF for all fields"""
    from fields.models import Field
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph("Farm Summary Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # All Fields Summary
    fields = Field.objects.all()
    
    fields_data = [['Field Name', 'Location', 'Size (acres)', 'Soil Type', 'Irrigation']]
    for field in fields:
        fields_data.append([
            field.name,
            field.location[:25],
            f'{field.size_acres}',
            field.soil_type,
            field.irrigation_type
        ])
    
    fields_table = Table(fields_data, colWidths=[1.5*inch, 1.8*inch, 1*inch, 1*inch, 1*inch])
    fields_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(fields_table)
    
    # Footer
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    footer = Paragraph(footer_text, styles['Normal'])
    elements.append(Spacer(1, 30))
    elements.append(footer)
    
    # Build PDF
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
