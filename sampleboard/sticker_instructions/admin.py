from django.contrib import admin
from .models import InstructionsPDF, Sticker

@admin.register(InstructionsPDF)
class InstructionsPDFAdmin(admin.ModelAdmin):
    list_display = ['id', 'marker', 'pdf_file']
    

@admin.register(Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sample_board', 'image']
    

