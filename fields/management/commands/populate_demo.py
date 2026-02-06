"""
Quick demo data creation for Indian agriculture - streamlined version
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random

from fields.models import Field, CropHistory
from soil.models import SoilAnalysis
from calendar_weather.models import WeatherData, CropCalendar
from rotation.models import RotationPlan, RotationSequence, RotationBenefit
from analytics.models import FinancialRecord, PerformanceMetric, YieldForecast


class Command(BaseCommand):
    help = 'Quick populate with Indian demo data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🇮🇳 Creating Indian Agricultural Demo Data...'))
        
        # Clear existing
        Field.objects.all().delete()
        
        # Create 6 Indian fields
        fields_data = [
            ('Punjab Wheat Belt', 'Lud hiana, Punjab', 25.5, 'Loamy', 'Canal Irrigation'),
            ('Maharashtra Sugarcane Estate', 'Kolhapur, Maharashtra', 18.0, 'Black Soil', 'Drip Irrigation'),
            ('Tamil Nadu Rice Paddy', 'Thanjavur, Tamil Nadu', 12.3, 'Clay', 'Flood Irrigation'),
            ('Gujarat Cotton Field', 'Ahmedabad, Gujarat', 22.0, 'Sandy Loam', 'Sprinkler'),
            ('Uttar Pradesh Mixed Farm', 'Meerut, Uttar Pradesh', 15.8, 'Alluvial', 'Tube Well'),
            ('Karnataka Vegetable Garden', 'Bangalore Rural, Karnataka', 8.5, 'Red Soil', 'Drip Irrigation'),
        ]
        
        fields = []
        for name, location, size, soil_type, irrigation in fields_data:
            field = Field.objects.create(
                name=name,
                location=location,
                size_acres=Decimal(str(size)),
                soil_type=soil_type,
                irrigation_type=irrigation
            )
            fields.append(field)
        
        self.stdout.write(f'✓ Created {len(fields)} fields')
        
        # Create crop history
        crops = ['Rice (Basmati)', 'Wheat', 'Sugarcane', 'Cotton', 'Tomato', 'Chickpea']
        for field in fields:
            for i in range(3):
                days_ago = random.randint(90, 730)
                CropHistory.objects.create(
                    field=field,
                    crop_name=random.choice(crops),
                    variety=f'Variety-{i+1}',
                    planting_date=timezone.now().date() - timedelta(days=days_ago+120),
                    harvest_date=timezone.now().date() - timedelta(days=days_ago),
                    yield_amount=Decimal(str(random.randint(800, 1500))),
                    notes='Kharif/Rabi season'
                )
        
        self.stdout.write(f'✓ Created {CropHistory.objects.count()} crop records')
        
        # Create soil analyses
        for field in fields:
            for i in range(2):
                SoilAnalysis.objects.create(
                    field=field,
                    analysis_date=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                    ph_level=Decimal(str(round(random.uniform(6.0, 7.5), 1))),
                    nitrogen_ppm=Decimal(str(round(random.uniform(30, 60), 1))),
                    phosphorus_ppm=Decimal(str(round(random.uniform(20, 45), 1))),
                    potassium_ppm=Decimal(str(round(random.uniform(150, 300), 1))),
                    organic_matter_percent=Decimal(str(round(random.uniform(2.0, 4.0), 1))),
                    recommendations='Add organic manure for better yields'
                )
        
        self.stdout.write(f'✓ Created {SoilAnalysis.objects.count()} soil analyses')
        
        # Create weather data
        for field in fields[:3]:  # Only first 3 fields
            for i in range(30):  # Last 30 days
                WeatherData.objects.create(
                    field=field,
                    date=timezone.now().date() - timedelta(days=i),
                    temperature_high=Decimal(str(round(random.uniform(28, 38), 1))),
                    temperature_low=Decimal(str(round(random.uniform(18, 25), 1))),
                    rainfall_mm=Decimal(str(round(random.uniform(0, 50), 1))),
                    humidity_percent=random.randint(50, 85),
                    condition=random.choice(['sunny', 'partly_cloudy', 'rainy'])
                )
        
        self.stdout.write(f'✓ Created {WeatherData.objects.count()} weather records')
        
        # Create calendar activities
        for field in fields:
            for activity_type in ['plowing', 'sowing', 'harvesting']:
                CropCalendar.objects.create(
                    field=field,
                    activity_type=activity_type,
                    crop_name=random.choice(crops),
                    scheduled_date=timezone.now().date() + timedelta(days=random.randint(5, 60)),
                    status='planned',
                    notes=f'Scheduled {activity_type}'
                )
        
        self.stdout.write(f'✓ Created {CropCalendar.objects.count()} calendar activities')
        
        # Create rotation plans
        for field in fields[:3]:
            plan = RotationPlan.objects.create(
                field=field,
                name=f'{field.name} - 3 Year Rotation',
                start_year=2024,
                duration_years=3,
                primary_goal='balanced',
                status='active',
                ai_generated=True,
                ai_confidence_score=85
            )
            
            for year in range(1, 4):
                RotationSequence.objects.create(
                    rotation_plan=plan,
                    year_in_rotation=year,
                    crop_name=random.choice(crops),
                    planting_season='kharif',
                    expected_yield_kg_per_acre=Decimal(str(random.randint(800, 1200)))
                )
        
        self.stdout.write(f'✓ Created {RotationPlan.objects.count()} rotation plans')
        
        # Create financial records in INR
        for field in fields:
            # Income
            for _ in range(3):
                FinancialRecord.objects.create(
                    field=field,
                    transaction_type='income',
                    category='crop_sales',
                    amount=Decimal(str(random.randint(40000, 80000))),
                    date=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                    description='Crop harvest sale',
                    payment_method='bank_transfer'
                )
            
            # Expenses
            for category in ['seeds', 'fertilizer', 'labor']:
                FinancialRecord.objects.create(
                    field=field,
                    transaction_type='expense',
                    category=category,
                    amount=Decimal(str(random.randint(5000, 15000))),
                    date=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                    description=f'{category.capitalize()} purchase',
                    payment_method='cash'
                )
        
        self.stdout.write(f'✓ Created {FinancialRecord.objects.count()} financial records')
        
        # Create performance metrics
        for field in fields:
            for metric_type in ['yield_efficiency', 'soil_health_score', 'profitability']:
                PerformanceMetric.objects.create(
                    field=field,
                    metric_type=metric_type,
                    score=Decimal(str(round(random.uniform(65, 92), 2))),
                    measurement_date=timezone.now().date(),
                    year=timezone.now().year,
                    month=timezone.now().month,
                    notes='Auto-generated metric'
                )
        
        self.stdout.write(f'✓ Created {PerformanceMetric.objects.count()} performance metrics')
        
        # Create yield forecasts
        for field in fields:
            for year_offset in [1, 2]:
                YieldForecast.objects.create(
                    field=field,
                    crop_name=random.choice(crops),
                    forecast_year=timezone.now().year + year_offset,
                    planting_season='spring',
                    predicted_yield_kg=Decimal(str(random.randint(8000, 20000))),
                    confidence_level=random.randint(75, 92),
                    prediction_method='trend_analysis'
                )
        
        self.stdout.write(f'✓ Created {YieldForecast.objects.count()} yield forecasts')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Demo Data Complete!'))
        self.stdout.write(self.style.SUCCESS('🌾 Indian agricultural demo data is ready!'))
        self.stdout.write(self.style.SUCCESS(f'   • {len(fields)} Fields across Indian states'))
        self.stdout.write(self.style.SUCCESS(f'   • {CropHistory.objects.count()} Crop histories'))
        self.stdout.write(self.style.SUCCESS(f'   • {FinancialRecord.objects.count()} Financial transactions'))
        self.stdout.write(self.style.SUCCESS(f'   • Visit http://localhost:8000/ to explore!'))
