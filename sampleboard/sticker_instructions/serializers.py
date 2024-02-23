from rest_framework import serializers

from core.models import Marker
from .models import InstructionsPDF, Sticker, HTMLCode

class InstructionsPDFSerializer(serializers.ModelSerializer):
    marker_id = serializers.PrimaryKeyRelatedField(queryset=Marker.objects.all())
    marker_number = serializers.CharField(source='marker.number', read_only=True)

    class Meta:
        model = InstructionsPDF
        fields = ['id','marker_id', 'marker_number', 'pdf_file']

    def create(self, validated_data):
        marker_id = validated_data.pop('marker_id')
        marker = marker_id if isinstance(marker_id, Marker) else Marker.objects.get(pk=marker_id)
        validated_data['marker'] = marker
        return super().create(validated_data)

class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = ['id', 'name', 'sample_board', 'image', 'order']


class HTMLCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTMLCode
        fields = ['id', 'sample_board','html_code']