from rest_framework import serializers
from .models import InstructionsPDF, Sticker

class InstructionsPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionsPDF
        fields = ['id', 'marker', 'pdf_file']

class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['id', 'name', 'sample_board', 'image']