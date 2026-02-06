from django.urls import path
from . import views

app_name = 'rotation'

urlpatterns = [
    # Dashboard
    path('', views.rotation_dashboard, name='dashboard'),
    
    # Rotation Plans
    path('plans/', views.rotation_plan_list, name='plan_list'),
    path('plans/<int:pk>/', views.rotation_plan_detail, name='plan_detail'),
    path('plans/create/', views.rotation_plan_create, name='plan_create'),
    path('plans/<int:pk>/edit/', views.rotation_plan_update, name='plan_update'),
    path('plans/<int:pk>/delete/', views.rotation_plan_delete, name='plan_delete'),
    
    # Rotation Sequences
    path('plans/<int:plan_id>/sequences/add/', views.sequence_create, name='sequence_create'),
    path('sequences/<int:pk>/edit/', views.sequence_update, name='sequence_update'),
    path('sequences/<int:pk>/delete/', views.sequence_delete, name='sequence_delete'),
    path('sequences/<int:pk>/complete/', views.sequence_mark_complete, name='sequence_complete'),
    
    # Benefits
    path('plans/<int:plan_id>/benefits/add/', views.benefit_create, name='benefit_create'),
    path('benefits/<int:pk>/edit/', views.benefit_update, name='benefit_update'),
    path('benefits/', views.benefit_list, name='benefit_list'),
    
    # AI Generation
    path('generate/', views.generate_rotation_view, name='generate'),
    
    # API
    path('plans/<int:pk>/timeline-data/', views.rotation_timeline_data, name='timeline_data'),
]
