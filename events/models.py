from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    # From your notes:
    name = models.CharField(max_length=200)
    image_url = models.URLField() # Image link
    description = models.TextField() # Detailed Description
    capacity = models.IntegerField() # Capacity
    
    # Tracking:
    current_signups = models.IntegerField(default=0)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name