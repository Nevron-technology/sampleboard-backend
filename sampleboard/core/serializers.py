from rest_framework import serializers
from .models import Marker, SampleBoard, Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name', 'hex_color']


class MarkerSerializer(serializers.ModelSerializer):
    type_info = TypeSerializer(source='type', read_only=True)

    class Meta:
        model = Marker
        fields = ['id', 'latitude', 'longitude', 'number', 'type', 'type_info']


class SampleBoardSerializer(serializers.ModelSerializer):
    marker = serializers.PrimaryKeyRelatedField(queryset=Marker.objects.all())
    
    class Meta:
        model = SampleBoard
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']