from rest_framework import serializers
from .models import InstructionsPDF, Sticker, HTMLCode

class InstructionsPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionsPDF
        fields = ['id', 'marker', 'pdf_file']


class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['id', 'name', 'sample_board', 'image', 'order']


class HTMLCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTMLCode
        fields = ['id', 'sample_board','html_code']