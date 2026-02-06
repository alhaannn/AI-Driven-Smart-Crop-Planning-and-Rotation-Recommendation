"""
Simple demo data - no calendar weather to avoid M2M issues
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random

from fields.models import Field, CropHistory
from soil.models import SoilAnalysis
from analytics.models import FinancialRecord, PerformanceMetric, YieldForecast


class Command(BaseCommand):
    help = 'Simple Indian demo data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🇮🇳 Creating Demo Data...'))
        
        # Clear existing
        self.stdout.write('Clearing old data...')
        Field.objects.all().delete()
        
        # Create fields
        self.stdout.write('Creating fields...')
        fields = []
        field_names = [
            ('Punjab Wheat Belt', 'Ludhiana, Punjab', 25.5),
            ('Maharashtra Farm', 'Kolhapur, Maharashtra', 18.0),
            ('Tamil Nadu Paddy', 'Thanjavur, Tamil Nadu', 12.3),
        ]
        
        for name, location, size in field_names:
            field = Field.objects.create(
                name=name,
                location=location,
                size_acres=Decimal(str(size)),
                soil_type='Loamy',
                irrigation_type='Canal'
            )
            fields.append(field)
        
        self.stdout.write(f'✓ {len(fields)} fields')
        
        # Crop history
        for field in fields:
            for i in range(3):
                CropHistory.objects.create(
                    field=field,
                    crop_name=random.choice(['Rice', 'Wheat', 'Cotton']),
                    planting_date=timezone.now().date() - timedelta(days=200),
                    harvest_date=timezone.now().date() - timedelta(days=100),
                    yield_amount=Decimal(str(random.randint(1000, 1500)))
                )
        
        self.stdout.write(f'✓ {CropHistory.objects.count()} crops')
        
        # Soil
        for field in fields:
            SoilAnalysis.objects.create(
                field=field,
                analysis_date=timezone.now().date(),
                ph_level=Decimal('6.8'),
                nitrogen_ppm=Decimal('45'),
                phosphorus_ppm=Decimal('30'),
                potassium_ppm=Decimal('220'),
                organic_matter=Decimal('3.2')
            )
        
        self.stdout.write(f'✓ {SoilAnalysis.objects.count()} soil analyses')
        
        # Financial
        for field in fields:
            FinancialRecord.objects.create(
                field=field,
                transaction_type='income',
                category='crop_sales',
                amount=Decimal('50000'),
                date=timezone.now().date()
            )
            FinancialRecord.objects.create(
                field=field,
                transaction_type='expense',
                category='seeds',
                amount=Decimal('10000'),
                date=timezone.now().date()
            )
        
        self.stdout.write(f'✓ {FinancialRecord.objects.count()} financial records')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Complete! Visit http://localhost:8000/'))
