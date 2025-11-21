from django.core.management.base import BaseCommand
from core.models import Country, Region, City, Address, Hotel, HotelDetail, RoomType, RatePlan, RatePlanRate, User
import datetime

class Command(BaseCommand):
    help = 'Seed database with sample data (hotels, room types, rate plans)'

    def handle(self, *args, **options):
        # Create sample data if not exists
        if not Country.objects.filter(name='India').exists():
            c = Country.objects.create(iso_code='IN', name='India')
            r = Region.objects.create(country=c, name='Maharashtra')
            city = City.objects.create(region=r, name='Mumbai')
            addr = Address.objects.create(street='Sample St', city=city, postal_code='400001')
            for i in range(1,101):
                h = Hotel.objects.create(name=f'Hotel {i}', slug=f'hotel-{i}', address=addr, status='published')
                HotelDetail.objects.create(hotel=h, description='Sample hotel', checkin_time='14:00', checkout_time='12:00')
                for j in range(1,4):
                    rt = RoomType.objects.create(hotel=h, code=f'RT{j}', name=f'Room {j}', max_adults=2)
                    rp = RatePlan.objects.create(hotel=h, code=f'RP{j}', name='Standard')
                    RatePlanRate.objects.create(rate_plan=rp, date_from=datetime.date.today(), date_to=datetime.date.today()+datetime.timedelta(days=30), price=5000)
            self.stdout.write(self.style.SUCCESS('Seeded sample data'))
        else:
            self.stdout.write(self.style.WARNING('Data already seeded'))
