from django.db import models
from django.utils import timezone

class Booking(models.Model):
    SERVICE_CHOICES = [
        ('lawn-mowing', 'Lawn Mowing'),
        ('garden-maintenance', 'Garden Maintenance'),
        ('hedge-trimming', 'Hedge Trimming'),
        ('weed-control', 'Weed Control'),
        ('waste-removal', 'Waste Removal'),
        ('custom-landscaping', 'Custom Landscaping / Other'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    preferred_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    
    # CRM Ready Fields
    created_at = models.DateTimeField(auto_now_add=True)
    next_service_date = models.DateField(blank=True, null=True, help_text="For future CRM reminders")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.get_service_display()} on {self.preferred_date}"