from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


class Marker(models.Model):
    COLOR_CHOICES = (
    ('red', 'Red'),
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('orange', 'Orange'),
    ('purple', 'Purple'),
    ('pink', 'Pink'),
    ('brown', 'Brown'),
    ('black', 'Black'),
    ('white', 'White'),
    # Add more colors as needed 
    )   
    
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=500, null=True, blank=True)
    number = models.CharField(max_length=500, null=True, blank=True)
    type = models.CharField(max_length=50, choices=COLOR_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.number}'


class SampleBoard(TimeStampedModel):
    marker = models.ForeignKey(Marker,on_delete=models.CASCADE, null=True, blank=True)
    version = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return f'Sample board at marker {self.marker}'
