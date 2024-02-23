from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Marker, SampleBoard


class InstructionsPDF(models.Model):
    marker = models.OneToOneField(Marker,on_delete=models.CASCADE, null=True, blank=True)
    pdf_file = models.FileField(upload_to='instruction_pdfs/', null=True, blank=True)
    
    def __str__(self):
        return f'Instruction pdf at marker {self.marker}'


class Sticker(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    sample_board = models.ForeignKey(SampleBoard,on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='sticker_images/')
    order = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.name}'
    

class HTMLCode(models.Model):
    sample_board = models.OneToOneField(SampleBoard, on_delete=models.CASCADE, null=True, blank=True)
    html_code = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'HTML code for {self.sample_board}'



@receiver(post_save, sender=SampleBoard)
def create_html_code(sender, instance, created, **kwargs):
    if created:
        HTMLCode.objects.create(sample_board=instance)