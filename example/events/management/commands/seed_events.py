import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.utils import timezone
from events.models import Event
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with 15 sample events (10 Free, 5 Paid) using Naira prices.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Get or create an organizer
        organizer = User.objects.filter(is_superuser=True).first()
        if not organizer:
            # Fallback to the first user if superuser doesn't exist/isn't found
            organizer = User.objects.first()
            if not organizer:
                self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
                return

        self.stdout.write(f'Seeding events for organizer: {organizer.username}...')

        # Event data templates
        events_data = [
            # 5 Paid Events
            {"title": "Campus Music Festival", "desc": "Night of music and food!", "price": 5000.00, "type": "PAID", "cat": "music"},
            {"title": "Grand Gala Dinner", "desc": "Annual end-of-year formal dinner.", "price": 15000.00, "type": "PAID", "cat": "party"},
            {"title": "Tech Masterclass", "desc": "Advanced Python & AI workshop.", "price": 25000.00, "type": "PAID", "cat": "tech"},
            {"title": "Cinema Night: Premiere", "desc": "Exclusive screening of the latest blockbuster.", "price": 3000.00, "type": "PAID", "cat": "movie"},
            {"title": "VIP Networking Brunch", "desc": "Connect with industry leaders over brunch.", "price": 10000.00, "type": "PAID", "cat": "business"},
            
            # 10 Free Events
            {"title": "Freshers Orientation", "desc": "Welcome guide for new students.", "price": 0.00, "type": "FREE", "cat": "school"},
            {"title": "Library Book Club", "desc": "Weekly discussion on selected readings.", "price": 0.00, "type": "FREE", "cat": "book"},
            {"title": "Campus Clean-up Drive", "desc": "Volunteer to keep our campus green.", "price": 0.00, "type": "FREE", "cat": "nature"},
            {"title": "Morning Yoga Session", "desc": "Start your day with mindfulness.", "price": 0.00, "type": "FREE", "cat": "yoga"},
            {"title": "Career Fair 2026", "desc": "Meet recruiters from top companies.", "price": 0.00, "type": "FREE", "cat": "job"},
            {"title": "Open Mic Night", "desc": "Showcase your talent! Poetry, music, comedy.", "price": 0.00, "type": "FREE", "cat": "mic"},
            {"title": "Study Group: Calculus", "desc": "exam prep group study.", "price": 0.00, "type": "FREE", "cat": "math"},
            {"title": "Art Exhibition Opening", "desc": "Support local student artists.", "price": 0.00, "type": "FREE", "cat": "art"},
            {"title": "Debate Club Meetup", "desc": "Topic: AI Ethics.", "price": 0.00, "type": "FREE", "cat": "debate"},
            {"title": "End of Semester Party", "desc": "Celebrate surviving the exams!", "price": 0.00, "type": "FREE", "cat": "party"},
        ]

        # Process each event
        for i, data in enumerate(events_data):
            # Check if event exists to avoid duplicates if run multiple times without clearing
            if Event.objects.filter(title=data['title']).exists():
                 self.stdout.write(self.style.WARNING(f"Event '{data['title']}' already exists. Skipping."))
                 continue

            self.stdout.write(f"Creating event ({i+1}/15): {data['title']}")
            
            # Create Event instance
            event = Event(
                title=data['title'],
                description=data['desc'] + " " + "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                price=data['price'],
                event_type=data['type'],
                capacity=random.randint(50, 500),
                organizer=organizer,
                event_date=timezone.now() + timedelta(days=i*3 + 2)
            )

            # Use Picsum for reliable random images
            # Adding a random seed to URL ensures we get different images but they are stable per run if needed
            image_url = f"https://picsum.photos/seed/{i+100}/800/600"

            try:
                # User-Agent is good practice even for Picsum
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(image_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    file_name = f"event_{i}_{random.randint(1000,9999)}.jpg"
                    event.image.save(file_name, ContentFile(response.content), save=False)
                else:
                    self.stdout.write(self.style.WARNING(f"Failed to download image for {data['title']}: Status {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Error downloading image: {e}"))

            event.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully created '{data['title']}'"))

        self.stdout.write(self.style.SUCCESS('Seeding complete! 15 Events Created.'))
