"""
Django management command to populate database with Indian agricultural demo data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import random

from fields.models import Field, CropHistory
from soil.models import SoilAnalysis
from calendar_weather.models import WeatherData, CropCalendar, CropRecommendation
from rotation.models import RotationPlan, RotationSequence, RotationBenefit
from analytics.models import FinancialRecord, PerformanceMetric, YieldForecast


class Command(BaseCommand):
    help = 'Populate database with Indian agricultural demo data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🇮🇳 Starting Indian Agricultural Demo Data Population...'))
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        self.stdout.write('Clearing existing data...')
        Field.objects.all().delete()
        
        # Create Indian Fields
        self.stdout.write('Creating fields in different Indian states...')
        fields = self.create_fields()
        
        # Create Crop History
        self.stdout.write('Creating crop history with Indian crops...')
        self.create_crop_history(fields)
        
        # Create Soil Analyses
        self.stdout.write('Creating soil analysis data...')
        self.create_soil_analyses(fields)
        
        # Create Weather Data
        self.stdout.write('Creating weather data for Indian climate...')
        self.create_weather_data(fields)
        
        # Create Calendar Activities
        self.stdout.write('Creating crop calendar activities...')
        self.create_calendar_activities(fields)
        
        # Create Crop Recommendations
        # self.stdout.write('Creating crop recommendations...')
        # self.create_recommendations(fields)
        
        # Create Rotation Plans
        self.stdout.write('Creating crop rotation plans...')
        self.create_rotation_plans(fields)
        
        # Create Financial Records
        self.stdout.write('Creating financial records in INR...')
        self.create_financial_records(fields)
        
        # Create Performance Metrics
        self.stdout.write('Creating performance metrics...')
        self.create_performance_metrics(fields)
        
        # Create Yield Forecasts
        self.stdout.write('Creating yield forecasts...')
        self.create_yield_forecasts(fields)
        
        self.stdout.write(self.style.SUCCESS('✅ Demo data population complete!'))
        self.stdout.write(self.style.SUCCESS('🌾 Indian agricultural data is ready to explore!'))

    def create_fields(self):
        """Create fields in different Indian states"""
        indian_fields = [
            {
                'name': 'Punjab Wheat Belt',
                'location': 'Ludhiana, Punjab',
                'size_acres': Decimal('25.5'),
                'soil_type': 'Loamy',
                'irrigation_type': 'Canal Irrigation'
            },
            {
                'name': 'Maharashtra Sugarcane Estate',
                'location': 'Kolhapur, Maharashtra',
                'size_acres': Decimal('18.0'),
                'soil_type': 'Black Soil',
                'irrigation_type': 'Drip Irrigation'
            },
            {
                'name': 'Tamil Nadu Rice Paddy',
                'location': 'Thanjavur, Tamil Nadu',
                'size_acres': Decimal('12.3'),
                'soil_type': 'Clay',
                'irrigation_type': 'Flood Irrigation'
            },
            {
                'name': 'Gujarat Cotton Field',
                'location': 'Ahmedabad, Gujarat',
                'size_acres': Decimal('22.0'),
                'soil_type': 'Sandy Loam',
                'irrigation_type': 'Sprinkler'
            },
            {
                'name': 'Uttar Pradesh Mixed Farm',
                'location': 'Meerut, Uttar Pradesh',
                'size_acres': Decimal('15.8'),
                'soil_type': 'Alluvial',
                'irrigation_type': 'Tube Well'
            },
            {
                'name': 'Karnataka Vegetable Garden',
                'location': 'Bangalore Rural, Karnataka',
                'size_acres': Decimal('8.5'),
                'soil_type': 'Red Soil',
                'irrigation_type': 'Drip Irrigation'
            }
        ]
        
        fields = []
        for field_data in indian_fields:
            field = Field.objects.create(**field_data)
            fields.append(field)
            self.stdout.write(f'  ✓ Created: {field.name}')
        
        return fields

    def create_crop_history(self, fields):
        """Create crop history with Indian crops"""
        indian_crops = [
            # Cereals
            {'name': 'Rice (Basmati)', 'variety': 'Pusa Basmati 1121', 'season': 'Kharif'},
            {'name': 'Wheat', 'variety': 'HD 2967', 'season': 'Rabi'},
            {'name': 'Jowar', 'variety': 'CSH 16', 'season': 'Kharif'},
            {'name': 'Bajra', 'variety': 'HHB 67', 'season': 'Kharif'},
            
            # Cash Crops
            {'name': 'Sugarcane', 'variety': 'Co 86032', 'season': 'Annual'},
            {'name': 'Cotton', 'variety': 'Bt Cotton', 'season': 'Kharif'},
            {'name': 'Jute', 'variety': 'JRO 524', 'season': 'Kharif'},
            
            # Pulses
            {'name': 'Chickpea (Chana)', 'variety': 'JG 11', 'season': 'Rabi'},
            {'name': 'Pigeon Pea (Arhar)', 'variety': 'ICPL 87119', 'season': 'Kharif'},
            {'name': 'Green Gram (Moong)', 'variety': 'TM 96-2', 'season': 'Kharif'},
            
            # Vegetables
            {'name': 'Tomato', 'variety': 'Pusa Ruby', 'season': 'Rabi'},
            {'name': 'Potato', 'variety': 'Kufri Jyoti', 'season': 'Rabi'},
            {'name': 'Onion', 'variety': 'N 53', 'season': 'Rabi'},
        ]
        
        for field in fields:
            # Create 3-5 historical harvests per field
            num_harvests = random.randint(3, 5)
            for i in range(num_harvests):
                crop = random.choice(indian_crops)
                days_ago = random.randint(90, 730)  # 3 months to 2 years ago
                
                planting_date = timezone.now().date() - timedelta(days=days_ago + 120)
                harvest_date = timezone.now().date() - timedelta(days=days_ago)
                
                # Realistic Indian yields (kg per acre)
                yield_ranges = {
                    'Rice (Basmati)': (800, 1200),
                    'Wheat': (1200, 1800),
                    'Sugarcane': (25000, 35000),
                    'Cotton': (400, 600),
                    'Tomato': (8000, 12000),
                    'Potato': (6000, 9000),
                    'Chickpea (Chana)': (600, 900),
                }
                
                base_yield = yield_ranges.get(crop['name'], (500, 1500))
                yield_per_acre = Decimal(str(random.uniform(*base_yield)))
                total_yield = yield_per_acre * field.size_acres
                
                CropHistory.objects.create(
                    field=field,
                    crop_name=crop['name'],
                    variety=crop['variety'],
                    planting_date=planting_date,
                    harvest_date=harvest_date,
                    yield_amount=yield_per_acre,
                    notes=f"{crop['season']} season harvest"
                )
        
        self.stdout.write(f'  ✓ Created {CropHistory.objects.count()} crop history records')

    def create_soil_analyses(self, fields):
        """Create soil analysis data typical of Indian soils"""
        soil_characteristics = {
            'Loamy': {'ph': (6.5, 7.5), 'n': (40, 60), 'p': (25, 45), 'k': (200, 300)},
            'Black Soil': {'ph': (7.0, 8.5), 'n': (30, 50), 'p': (20, 40), 'k': (250, 400)},
            'Clay': {'ph': (6.0, 7.0), 'n': (35, 55), 'p': (15, 35), 'k': (150, 250)},
            'Sandy Loam': {'ph': (6.0, 7.0), 'n': (25, 45), 'p': (10, 30), 'k': (100, 200)},
            'Alluvial': {'ph': (6.5, 7.8), 'n': (45, 70), 'p': (30, 50), 'k': (200, 350)},
            'Red Soil': {'ph': (5.5, 6.5), 'n': (20, 40), 'p': (12, 28), 'k': (80, 180)},
        }
        
        for field in fields:
            # Create 2-3 soil analyses per field
            for i in range(random.randint(2, 3)):
                days_ago = random.randint(30, 365)
                analysis_date = timezone.now().date() - timedelta(days=days_ago)
                
                soil_params = soil_characteristics.get(field.soil_type, 
                    {'ph': (6.0, 7.0), 'n': (30, 50), 'p': (20, 40), 'k': (150, 250)})
                
                SoilAnalysis.objects.create(
                    field=field,
                    analysis_date=analysis_date,
                    ph_level=Decimal(str(round(random.uniform(*soil_params['ph']), 1))),
                    nitrogen_ppm=Decimal(str(round(random.uniform(*soil_params['n']), 1))),
                    phosphorus_ppm=Decimal(str(round(random.uniform(*soil_params['p']), 1))),
                    potassium_ppm=Decimal(str(round(random.uniform(*soil_params['k']), 1))),
                    organic_matter_percent=Decimal(str(round(random.uniform(1.5, 4.5), 1))),
                    recommendations=f"Suitable for {field.name.split()[1]} cultivation. "
                                  f"Consider adding organic manure for better yields."
                )
        
        self.stdout.write(f'  ✓ Created {SoilAnalysis.objects.count()} soil analyses')

    def create_weather_data(self, fields):
        """Create weather data for Indian climate"""
        # Indian weather patterns
        for field in fields:
            # Create weather data for last 60 days
            for i in range(60):
                date = timezone.now().date() - timedelta(days=i)
                month = date.month
                
                # Indian seasonal temperature patterns (Celsius)
                if month in [12, 1, 2]:  # Winter
                    temp_range = (15, 25)
                    rainfall = random.uniform(0, 10) if random.random() < 0.2 else 0
                    conditions = ['sunny', 'partly_cloudy', 'cloudy']
                elif month in [3, 4, 5]:  # Summer
                    temp_range = (28, 42)
                    rainfall = random.uniform(0, 20) if random.random() < 0.3 else 0
                    conditions = ['sunny', 'hot', 'partly_cloudy']
                elif month in [6, 7, 8, 9]:  # Monsoon
                    temp_range = (25, 32)
                    rainfall = random.uniform(10, 150) if random.random() < 0.7 else random.uniform(0, 10)
                    conditions = ['rainy', 'heavy_rain', 'cloudy', 'partly_cloudy']
                else:  # Post-monsoon
                    temp_range = (20, 30)
                    rainfall = random.uniform(0, 30) if random.random() < 0.3 else 0
                    conditions = ['sunny', 'partly_cloudy', 'cloudy']
                
                WeatherData.objects.create(
                    field=field,
                    date=date,
                    temperature_high=Decimal(str(round(random.uniform(temp_range[0] + 5, temp_range[1]), 1))),
                    temperature_low=Decimal(str(round(random.uniform(temp_range[0], temp_range[0] + 5), 1))),
                    rainfall_mm=Decimal(str(round(rainfall, 1))),
                    humidity_percent=random.randint(40, 90),
                    condition=random.choice(conditions)
                )
        
        self.stdout.write(f'  ✓ Created {WeatherData.objects.count()} weather records')

    def create_calendar_activities(self, fields):
        """Create agricultural calendar activities"""
        activities = [
            ('plowing', 'Kharif Plowing', 15),
            ('sowing', 'Kharif Sowing', 7),
            ('fertilizing', 'First Fertilizer Application', -10),
            ('irrigation', 'Monsoon Irrigation Check', -5),
            ('weeding', 'Mid-season Weeding', 20),
            ('harvesting', 'Kharif Harvest', 45),
            ('plowing', 'Rabi Plowing', 60),
            ('sowing', 'Rabi Sowing', 75),
        ]
        
        for field in fields:
            # Create activities
            for activity_type, description, days_offset in activities:
                scheduled_date = timezone.now().date() + timedelta(days=days_offset)
                
                # Determine status
                if days_offset < -5:
                    status = 'completed'
                    actual_date = scheduled_date
                elif days_offset < 0:
                    status = 'pending'
                    actual_date = None
                else:
                    status = 'planned'
                    actual_date = None
                
                CropCalendar.objects.create(
                    field=field,
                    activity_type=activity_type,
                    crop_name=random.choice(['Rice', 'Wheat', 'Cotton', 'Sugarcane']),
                    scheduled_date=scheduled_date,
                    completed_date=actual_date,
                    status=status,
                    notes=description
                )
        
        self.stdout.write(f'  ✓ Created {CropCalendar.objects.count()} calendar activities')

    def create_recommendations(self, fields):
        """Create crop recommendations"""
        recommendations = [
            {
                'crop': 'Rice (Basmati)',
                'season': 'kharif',
                'reason': 'High water availability during monsoon, suitable soil pH and nutrients',
                'confidence': 92
            },
            {
                'crop': 'Wheat',
                'season': 'rabi',
                'reason': 'Optimal winter temperatures, good soil fertility, established irrigation',
                'confidence': 88
            },
            {
                'crop': 'Cotton',
                'season': 'kharif',
                'reason': 'Suitable black soil, warm climate, adequate monsoon rainfall',
                'confidence': 85
            },
            {
                'crop': 'Sugarcane',
                'season': 'annual',
                'reason': 'Consistent irrigation, suitable climate, good market demand',
                'confidence': 80
            }
        ]
        
        for field in fields:
            # Create 2 recommendations per field
            for i, rec in enumerate(recommendations[:2]):
                CropRecommendation.objects.create(
                    field=field,
                    recommended_crop=rec['crop'],
                    suggested_season=rec['season'],
                    confidence_score=rec['confidence'],
                    reasoning=rec['reason']
                )
        
        self.stdout.write(f'  ✓ Created {CropRecommendation.objects.count()} recommendations')

    def create_rotation_plans(self, fields):
        """Create crop rotation plans"""
        for field in fields[:4]:  # Create plans for first 4 fields
            plan = RotationPlan.objects.create(
                field=field,
                name=f"{field.name} - 3 Year Rotation",
                start_year=2024,
                duration_years=3,
                primary_goal='balanced',
                status='active',
                ai_generated=True,
                ai_confidence_score=85,
                notes="AI-optimized rotation plan for Indian agricultural practices"
            )
            
            # Create rotation sequences
            crops_sequence = [
                ('Rice (Basmati)', 'kharif', 'Nitrogen depleting, high yield'),
                ('Chickpea (Chana)', 'rabi', 'Nitrogen fixing legume'),
                ('Wheat', 'rabi', 'Benefits from residual nitrogen'),
            ]
            
            for year, (crop, season, notes) in enumerate(crops_sequence, 1):
                RotationSequence.objects.create(
                    rotation_plan=plan,
                    year_in_rotation=year,
                    crop_name=crop,
                    planting_season=season,
                    expected_yield_kg_per_acre=Decimal(str(random.randint(800, 1500))),
                    notes=notes,
                    is_completed=(year == 1)
                )
            
            # Add benefits
            benefits = [
                ('soil_health', 15, 2, 7),
                ('yield_increase', 12, 3, 8),
                ('pest_reduction', 20, 2, 6),
            ]
            
            for benefit_type, improvement, year, priority in benefits:
                RotationBenefit.objects.create(
                    rotation_plan=plan,
                    benefit_type=benefit_type,
                    expected_improvement_percent=Decimal(str(improvement)),
                    expected_to_manifest_year=year,
                    priority=priority
                )
        
        self.stdout.write(f'  ✓ Created {RotationPlan.objects.count()} rotation plans')

    def create_financial_records(self, fields):
        """Create financial records in INR"""
        # Income records
        income_categories = [
            ('crop_sales', 'Rice harvest sale', 45000, 85000),
            ('crop_sales', 'Wheat harvest sale', 35000, 65000),
            ('subsidies', 'Government subsidy', 8000, 15000),
        ]
        
        # Expense records
        expense_categories = [
            ('seeds', 'Basmati rice seeds', 3000, 6000),
            ('fertilizer', 'NPK fertilizer', 8000, 15000),
            ('pesticides', 'Pesticide application', 4000, 8000),
            ('labor', 'Seasonal labor wages', 12000, 25000),
            ('irrigation', 'Electricity for tube well', 5000, 10000),
            ('fuel', 'Diesel for tractor', 6000, 12000),
        ]
        
        for field in fields:
            # Create income records
            for category, description, min_amt, max_amt in income_categories:
                for _ in range(random.randint(2, 4)):
                    days_ago = random.randint(30, 365)
                    FinancialRecord.objects.create(
                        field=field,
                        transaction_type='income',
                        category=category,
                        amount=Decimal(str(random.randint(min_amt, max_amt))),
                        date=timezone.now().date() - timedelta(days=days_ago),
                        description=description,
                        payment_method='bank_transfer'
                    )
            
            # Create expense records
            for category, description, min_amt, max_amt in expense_categories:
                for _ in range(random.randint(1, 3)):
                    days_ago = random.randint(30, 365)
                    FinancialRecord.objects.create(
                        field=field,
                        transaction_type='expense',
                        category=category,
                        amount=Decimal(str(random.randint(min_amt, max_amt))),
                        date=timezone.now().date() - timedelta(days=days_ago),
                        description=description,
                        payment_method=random.choice(['cash', 'bank_transfer', 'mobile_payment'])
                    )
        
        self.stdout.write(f'  ✓ Created {FinancialRecord.objects.count()} financial records')

    def create_performance_metrics(self, fields):
        """Create performance metrics"""
        metric_types = [
            'yield_efficiency',
            'soil_health_score',
            'profitability',
            'rotation_adherence'
        ]
        
        for field in fields:
            for metric_type in metric_types:
                PerformanceMetric.objects.create(
                    field=field,
                    metric_type=metric_type,
                    score=Decimal(str(round(random.uniform(60, 95), 2))),
                    measurement_date=timezone.now().date(),
                    year=timezone.now().year,
                    month=timezone.now().month,
                    calculation_details={'method': 'automated'},
                    notes='Auto-generated performance metric'
                )
        
        self.stdout.write(f'  ✓ Created {PerformanceMetric.objects.count()} performance metrics')

    def create_yield_forecasts(self, fields):
        """Create yield forecasts"""
        crops = ['Rice (Basmati)', 'Wheat', 'Cotton', 'Sugarcane']
        
        for field in fields:
            for year_offset in range(1, 3):
                YieldForecast.objects.create(
                    field=field,
                    crop_name=random.choice(crops),
                    forecast_year=timezone.now().year + year_offset,
                    planting_season=random.choice(['spring', 'summer', 'fall']),
                    predicted_yield_kg=Decimal(str(random.randint(5000, 25000))),
                    confidence_level=random.randint(70, 95),
                    prediction_method='trend_analysis',
                    factors_considered={
                        'historical_data': True,
                        'soil_health': True,
                        'weather_patterns': True
                    }
                )
        
        self.stdout.write(f'  ✓ Created {YieldForecast.objects.count()} yield forecasts')
