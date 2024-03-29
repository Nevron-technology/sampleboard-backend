from django.contrib import admin
from .models import Marker, SampleBoard, Type

@admin.register(Marker)
class MarkerAdmin(admin.ModelAdmin):
    list_display = ['id', 'latitude', 'longitude', 'number', 'type']
    

@admin.register(SampleBoard)
class SampleBoardAdmin(admin.ModelAdmin):
    list_display = ['id', 'marker', 'version']
    
admin.site.register(Type)

