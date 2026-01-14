from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()  # The "Instagram caption"
    image = models.URLField(blank=True)  # Link to event poster
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Ticketing / Social interaction
    attendees = models.ManyToManyField(User, related_name="tickets", blank=True)
    max_tickets = models.IntegerField(default=100)

    class Meta:
        ordering = ["-created_at"]  # Newest posts first (Insta style)
