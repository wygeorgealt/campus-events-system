from django.db import models
from django.contrib.auth.models import User
# The template uses this specific field for MongoDB compatibility
from django_mongodb_backend.fields import ObjectIdField, ObjectIdAutoField 

class Event(models.Model):
    # The template often handles the PK automatically, 
    # but defining it explicitly ensures no clashes.
    id = ObjectIdAutoField(primary_key=True, editable=False, blank=True)    
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='event_pics/')
    description = models.TextField()
    capacity = models.IntegerField()
    signed_up_count = models.IntegerField(default=0)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# Create your models here.
