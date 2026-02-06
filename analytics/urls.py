from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Dashboard
    path('', views.analytics_dashboard, name='dashboard'),
    
    # Financial Analytics
    path('financial/', views.financial_overview, name='financial_overview'),
    path('financial/add/', views.financial_record_create, name='financial_create'),
    path('financial/<int:pk>/edit/', views.financial_record_update, name='financial_update'),
    path('financial/<int:pk>/delete/', views.financial_record_delete, name='financial_delete'),
    
    # Yield Analysis
    path('yield/', views.yield_analysis, name='yield_analysis'),
    path('yield/forecast/add/', views.yield_forecast_create, name='forecast_create'),
    path('yield/forecast/<int:pk>/edit/', views.yield_forecast_update, name='forecast_update'),
    
    # Performance Metrics
    path('performance/', views.performance_metrics_view, name='performance_metrics'),
    
    # Insights
    path('insights/', views.insights_view, name='insights'),
]
