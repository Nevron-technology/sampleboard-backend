from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid

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

class Type(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    hex_color = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f'{self.name}'


class Marker(models.Model):
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=500, null=True, blank=True)
    number = models.CharField(max_length=500, unique=True, null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.number}'


class SampleBoard(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    marker = models.ForeignKey(Marker,on_delete=models.CASCADE, null=True, blank=True)
    version = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return f'Sample board at marker {self.marker}'


@receiver(post_save, sender=Marker)
def create_sample_board(sender, instance, created, **kwargs):
    if created:
        SampleBoard.objects.create(marker=instance, version="1.0")