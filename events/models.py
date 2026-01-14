from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    image_url = models.URLField() # For the Instagram-style photo
    description = models.TextField()
    capacity = models.IntegerField()
    signed_up_count = models.IntegerField(default=0)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title