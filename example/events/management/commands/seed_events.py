import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.utils import timezone
from events.models import Event
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with 8 sample events including images.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Get or create an organizer
        organizer = User.objects.filter(is_superuser=True).first()
        if not organizer:
            self.stdout.write(self.style.ERROR('No superuser found. Please create one field.'))
            return

        self.stdout.write(f'Seeding events for organizer: {organizer.username}...')

        events_data = [
            {
                "title": "Campus Music Festival",
                "description": "Join us for a night of music, food, and fun under the stars! Featuring local college bands.",
                "price": 15.00,
                "type": "PAID",
                "image_url": "https://images.unsplash.com/photo-1459749411177-2fe68d506b32?q=80&w=2070&auto=format&fit=crop",
                "bg_color": "1459749411177"
            },
            {
                "title": "Tech Paradox Symposium",
                "description": "Explore the future of AI and robotics with industry leaders.",
                "price": 0.00,
                "type": "FREE",
                "image_url": "https://images.unsplash.com/photo-1540575467063-17e6fc8a627c?q=80&w=2070&auto=format&fit=crop",
                 "bg_color": "1540575467063"
            },
            {
                "title": "Art & Design Showcase",
                "description": "A gallery walk-through of the finest student art projects of the semester.",
                "price": 5.00,
                "type": "PAID",
                "image_url": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?q=80&w=2080&auto=format&fit=crop",
                 "bg_color": "1460661419201"
            },
            {
                "title": "Codeathon 2026",
                "description": "24-hour coding marathon. Win prizes and get hired!",
                "price": 10.00,
                "type": "PAID",
                "image_url": "https://images.unsplash.com/photo-1504384308090-c54be3855833?q=80&w=2062&auto=format&fit=crop",
                 "bg_color": "1504384308090"
            },
            {
                "title": "Sustainability Workshop",
                "description": "Learn how to live a greener life on campus.",
                "price": 0.00,
                "type": "FREE",
                "image_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?q=80&w=2013&auto=format&fit=crop",
                 "bg_color": "1542601906990"
            },
            {
                "title": "Basketball Finals",
                "description": "Cheer for the home team in the season finale!",
                "price": 8.00,
                "type": "PAID",
                "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2090&auto=format&fit=crop",
                 "bg_color": "1546519638"
            },
            {
                "title": "Startup Pitch Night",
                "description": "Watch students pitch their business ideas to investors.",
                "price": 0.00,
                "type": "FREE",
                "image_url": "https://images.unsplash.com/photo-1559223607-a43c990ed91f?q=80&w=2070&auto=format&fit=crop",
                 "bg_color": "1559223607"
            },
             {
                "title": "Midnight Movie Screening",
                "description": "Relax with a classic movie at the student center.",
                "price": 2.00,
                "type": "PAID",
                "image_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=2025&auto=format&fit=crop",
                 "bg_color": "1536440136628"
            }
        ]

        for i, data in enumerate(events_data):
            # Check if event exists
            if Event.objects.filter(title=data['title']).exists():
                 self.stdout.write(self.style.WARNING(f"Event '{data['title']}' already exists. Skipping."))
                 continue

            self.stdout.write(f"Creating event: {data['title']}")
            
            # Create Event instance
            event = Event(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                event_type=data['type'],
                capacity=100 + (i * 50),
                organizer=organizer,
                event_date=timezone.now() + timedelta(days=i*7 + 2)
            )

            # Fetch image
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                response = requests.get(data['image_url'], headers=headers, timeout=10)
                if response.status_code == 200:
                    file_name = f"event_{data['bg_color']}.jpg"
                    event.image.save(file_name, ContentFile(response.content), save=False)
                else:
                    self.stdout.write(self.style.WARNING(f"Failed to download image for {data['title']}: Status {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error downloading image: {e}"))

            event.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully created '{data['title']}'"))

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
