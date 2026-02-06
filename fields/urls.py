from django.urls import path
from . import views

urlpatterns = [
    # Field URLs
    path('', views.field_list, name='field_list'),
    path('<int:pk>/', views.field_detail, name='field_detail'),
    path('create/', views.field_create, name='field_create'),
    path('<int:pk>/edit/', views.field_update, name='field_update'),
    path('<int:pk>/delete/', views.field_delete, name='field_delete'),
    
    # Crop History URLs
    path('crop-history/', views.crop_history_list, name='crop_history_list'),
    path('crop-history/<int:pk>/', views.crop_history_detail, name='crop_history_detail'),
    path('crop-history/create/', views.crop_history_create, name='crop_history_create'),
    path('crop-history/<int:pk>/edit/', views.crop_history_update, name='crop_history_update'),
    path('crop-history/<int:pk>/delete/', views.crop_history_delete, name='crop_history_delete'),
]
