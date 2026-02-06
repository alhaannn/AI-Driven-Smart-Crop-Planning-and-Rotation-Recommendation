from django.urls import path
from . import views

urlpatterns = [
    # Weather URLs
    path('weather/', views.weather_list, name='weather_list'),
    path('weather/<int:pk>/', views.weather_detail, name='weather_detail'),
    path('weather/create/', views.weather_create, name='weather_create'),
    path('weather/<int:pk>/edit/', views.weather_update, name='weather_update'),
    path('weather/<int:pk>/delete/', views.weather_delete, name='weather_delete'),
    
    # Calendar URLs
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/<int:pk>/', views.calendar_detail, name='calendar_detail'),
    path('calendar/create/', views.calendar_create, name='calendar_create'),
    path('calendar/<int:pk>/edit/', views.calendar_update, name='calendar_update'),
    path('calendar/<int:pk>/delete/', views.calendar_delete, name='calendar_delete'),
    path('calendar/<int:pk>/complete/', views.mark_complete, name='mark_complete'),
    
    # Recommendations URLs
    path('recommendations/', views.recommendations_view, name='recommendations_view'),
    path('recommendations/field/<int:field_id>/', views.recommendations_view, name='field_recommendations'),
    path('recommendations/generate/<int:field_id>/', views.generate_recommendations_view, name='generate_recommendations'),
    path('recommendations/<int:rec_id>/schedule/', views.schedule_from_recommendation, name='schedule_from_recommendation'),
]
