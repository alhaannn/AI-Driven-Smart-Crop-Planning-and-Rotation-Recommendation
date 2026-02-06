from django.urls import path
from . import views

urlpatterns = [
    # Soil Analysis URLs
    path('', views.soil_analysis_list, name='soil_analysis_list'),
    path('<int:pk>/', views.soil_analysis_detail, name='soil_analysis_detail'),
    path('create/', views.soil_analysis_create, name='soil_analysis_create'),
    path('<int:pk>/edit/', views.soil_analysis_update, name='soil_analysis_update'),
    path('<int:pk>/delete/', views.soil_analysis_delete, name='soil_analysis_delete'),
    
    # Recommendations
    path('recommendations/', views.recommendation_list, name='recommendation_list'),
    path('<int:pk>/regenerate/', views.regenerate_recommendations, name='regenerate_recommendations'),
    
    # Chart Data API
    path('<int:pk>/chart-data/', views.nutrient_chart_data, name='nutrient_chart_data'),
]
