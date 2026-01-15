from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django_mongodb_backend.fields import ObjectIdField, ObjectIdAutoField 
import uuid

class Event(models.Model):
    EVENT_TYPES = (
        ('FREE', 'Free Event'),
        ('PAID', 'Paid Event'),
    )

    id = ObjectIdAutoField(primary_key=True, editable=False, blank=True)    
    title = models.CharField(max_length=250)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default='FREE')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    description = models.TextField()
    capacity = models.IntegerField()
    signed_up_count = models.IntegerField(default=0)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __clstr__(self):
        return self.title

class Ticket(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"