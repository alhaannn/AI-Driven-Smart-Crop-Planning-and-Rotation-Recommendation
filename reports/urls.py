"""
URLs for reports app
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard
    path('', views.reports_dashboard, name='dashboard'),
    
    # PDF Exports
    path('pdf/field/<int:field_id>/', views.export_field_pdf, name='export_field_pdf'),
    path('pdf/financial/<int:field_id>/', views.export_financial_pdf, name='export_financial_pdf'),
    path('pdf/summary/', views.export_all_fields_pdf, name='export_all_fields_pdf'),
    
    # CSV Exports
    path('csv/fields/', views.export_fields_csv, name='export_fields_csv'),
    path('csv/crops/', views.export_crop_history_csv, name='export_crops_csv'),
    path('csv/crops/<int:field_id>/', views.export_crop_history_csv, name='export_field_crops_csv'),
    path('csv/soil/', views.export_soil_csv, name='export_soil_csv'),
    path('csv/soil/<int:field_id>/', views.export_soil_csv, name='export_field_soil_csv'),
    path('csv/financial/', views.export_financial_csv, name='export_financial_csv'),
    path('csv/financial/<int:field_id>/', views.export_financial_csv, name='export_field_financial_csv'),
    
    # Excel Exports
    path('excel/fields/', views.export_fields_excel, name='export_fields_excel'),
    path('excel/financial/', views.export_financial_excel, name='export_financial_excel'),
    path('excel/financial/<int:field_id>/', views.export_financial_excel, name='export_field_financial_excel'),
]
