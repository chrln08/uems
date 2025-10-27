from django.db import models
from datetime import datetime

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    location = models.CharField(max_length=255) # temporary
    archived = models.BooleanField(default=False)
    from_date = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d 00:00:00'))
    to_date = models.DateTimeField(default=datetime.now().strftime('%Y-%m-%d 00:00:00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name